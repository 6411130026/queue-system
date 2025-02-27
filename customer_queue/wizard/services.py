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
        """ ดึง Token ที่ยังไม่ถูกเรียกหรือไม่ถูก Skip มาแสดง """
        token_data = self.env['token.token'].search([('state', '=', 'registered')], order="id asc", limit=1)

        if not token_data:
            raise ValidationError(_("No available tokens. Please wait for the next patient.")) # แจ้งเตือนถ้าไม่มีคิวรอ

        # ตรวจสอบว่า Token นี้ถูกเรียกไปแล้วหรือไม่
        existing_token = self.customer_service_line_ids.filtered(lambda line: line.customer == token_data.name)
        if existing_token:
            raise ValidationError(_("This token has already been called."))  # ป้องกันการเรียกคิวซ้ำ

        department_id = token_data.department.id if token_data.department else False

        # อัปเดตค่าใน wizard
        self.write({
            'department_name': department_id,
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
            'res_id': self.id
        }

    def action_skip(self):
        """ ข้ามคิวปัจจุบัน และดึงคิวใหม่ขึ้นมา """
        token_data = self.env['token.token'].search([('state', '=', 'registered')], limit=1)

        if not token_data:
            raise ValidationError(_("No more tokens available to skip to."))

        # เปลี่ยน state ของคิวที่ถูกข้ามให้เป็น "Skipped"
        token_data.write({'state': 'skipped'})

        # ดึงคิวใหม่ที่ยังไม่ได้ Skip
        new_token = self.env['token.token'].search(
            [('state', '=', 'registered')], order="id asc", limit=1  # ไม่ใช้ offset=1 เพื่อให้เลือกคิวที่ถูกต้อง
        )

        if new_token:
            self.write({
                'customer_service_line_ids': [(0, 0, {
                    'customer': new_token.name,
                    'customer_name': new_token.customer_name,
                    'department': new_token.department.id if new_token.department else False,
                    'service_comment': new_token.service_comment,
                })]
            })
        else:
            raise ValidationError(_("No more tokens available after skipping."))

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'customer.service',
            'target': 'new',
            'res_id': self.id
        }


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


