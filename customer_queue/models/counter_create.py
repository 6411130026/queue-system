from odoo import fields, api, models, _

class CounterCreate(models.Model):
    _name = 'counter.counter'
    _description = "Counter Management"

    name = fields.Char(string="COUNTER", required=True, copy=False, index=True,
                       default=lambda self: _('New'))
    counter_name = fields.Char(string="Counter Name")
    department_name = fields.Many2one('hr.department', string="Department")
    state = fields.Selection([('create', 'Create'),
                              ('triage', 'Triage'),
                              ('consultation', 'Consultation'),
                              ('success', 'Success')], string="State", default='create', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('counter.sequence') or _('New')
        return super(CounterCreate, self).create(vals)

    def action_open_wizard(self):
        # ฟังก์ชันที่จะเปิดหน้าฟอร์ม (Wizard)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'customer.service',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_department_name': self.department_name.id,  # ส่ง department ไปใน context
                'default_counter': self.id,  # ส่งค่าของ counter ไปใน context
            },
        }

class CustomerService(models.TransientModel):
    _name = 'customer.service'

    counter = fields.Many2one('counter.counter', string='Counter')
    department_name = fields.Many2one('hr.department', string="Department")

    # กำหนดให้ฟอร์มเริ่มต้นด้วยค่าจาก context
    @api.model
    def default_get(self, fields):
        res = super(CustomerService, self).default_get(fields)

        # ตรวจสอบว่า context มีค่าของ default_counter และ default_department หรือไม่
        if self.env.context.get('default_counter'):
            res.update({'counter': self.env.context['default_counter']})

        if self.env.context.get('default_department_name'):
            res.update({'department_name': self.env.context['default_department_name']})

        return res
