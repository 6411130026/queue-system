from odoo import fields, api, SUPERUSER_ID, models, _
from odoo.exceptions import ValidationError


class CustomerService(models.TransientModel):
    _name = 'customer.service'

    user_name = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    date = fields.Datetime(default=fields.Datetime.now, string="Date")
    counter = fields.Many2one('counter.counter', string="Counter")
    department_name = fields.Many2one('hr.department', string="Department")
    customer_service_line_ids = fields.One2many('customer.service.line', 'customer_service_line_id', string="ids")

    def customer_service(self):
        """ ดึง Token มาแสดงใน Wizard และไม่ปิด Wizard ทันที """
        token_data = self.env['token.token'].search([('state', '=', 'registered')], limit=1)

        if not token_data:
            raise ValidationError(_("Not available token"))

        # ตรวจสอบว่า Token มี department หรือไม่
        department_id = token_data.department.id if token_data.department else False

        # อัปเดตค่าใน wizard
        self.write({
            'department_name': department_id,  # ตั้งค่า department ให้ตรงกับ Token
            'customer_service_line_ids': [(0, 0, {
                'customer': token_data.name,
                'customer_name': token_data.customer_name,
                'department': department_id,
                'service_comment': token_data.service_comment,
            })]
        })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'customer.service',
            'target': 'new',
            'res_id': self.id  # ให้ Odoo เปิด Wizard เดิมแทนที่จะปิด
        }

        # # ดึง state จาก department ที่เลือก
        # new_state = self.department_name.state_mapping
        # if not new_state:
        #     raise ValidationError(_("This department does not have a mapped state."))
        #
        # # อัปเดต state ของ token
        # token_data.write({'state': new_state})


class CustomerServiceLine(models.TransientModel):
    _name = 'customer.service.line'

    customer = fields.Char(string="Customer Token")
    customer_name = fields.Char(string="Customer Name")
    customer_mobile = fields.Integer(string="Mobile")
    customer_call = fields.Boolean(default=False, string="Call")
    service_comment = fields.Text(string="Service comment")
    customer_service_line_id = fields.Many2one('customer.service', string="id")
    department = fields.Many2one('hr.department', string="Department")

    def service_given(self):
        """ เมื่อกด 'Done' ให้เปลี่ยน state และอัปเดต department กลับไปที่ Token """
        token_data = self.env['token.token'].search([('name', '=', self.customer)], limit=1)

        if not token_data:
            raise ValidationError(_("Token not found."))

        if not self.department:
            raise ValidationError(_("Please select a department."))

        # ดึง state_mapping จาก department
        new_state = self.department.state_mapping
        if not new_state:
            raise ValidationError(_("This department does not have a mapped state."))

        # อัปเดต state และ department ของ Token
        token_data.write({
            'state': new_state,
            'department': self.department.id  # <-- อัปเดต department ที่เลือกกลับไปยัง token.token
        })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'customer.service',
            'target': 'new',
        }

    # def service_given(self):
    #     print("okkkk")
    #     token_data = self.env['token.token'].search([('state', '=', 'registered')])
    #     for rec in self:
    #         for token in token_data:
    #             if rec.customer == token.name:
    #                 token.write({'state': 'waiting_triage'})
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'customer.service',
    #         'target': 'new',
    #     }