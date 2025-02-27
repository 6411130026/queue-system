from odoo import fields, api, models, _


class TokenCreate(models.Model):
    _name = 'token.token'

    name = fields.Char(string="Queue ID", required=True, copy=False, randomly=True, index=True,
                       default=lambda self: _('New'))
    customer_name = fields.Char(string='Patient')
    customer_mobile = fields.Integer(string="Mobile")
    department = fields.Many2one('hr.department', string="Department")
    service_comment = fields.Text(string="Service comment")
    state = fields.Selection([('register', 'Register'),
                              ('registered', 'Registered'),
                              ('waiting_triage', 'Waiting for Triage'),
                              ('triage', 'Triage'),
                              ('waiting_cons', 'Waiting for Cons.'),
                              ('consultation', 'Consultation'),
                              ('waiting_payment', 'Waiting for Payment'),
                              ('paying', 'Payment in progress'),
                              ('skipped', 'Skipped'),
                              ('cancel', 'Cancel'),
                              ('done', 'Done')], string="State", default='register', tracking=True)

    @api.model
    def create(self, vals):
        """ เมื่อสร้าง Token ให้ตั้งค่า state ตาม department ที่เลือก """
        # ตรวจสอบว่ามีการเลือก department หรือไม่
        if 'department' in vals and vals['department']:
            department = self.env['hr.department'].browse(vals['department'])
            if department.state_mapping:
                vals['state'] = department.state_mapping  # อัปเดต state ตาม department

        # สร้าง Queue ID อัตโนมัติ
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('customer.sequence') or _('New')

        return super(TokenCreate, self).create(vals)

    def queue_confirm(self):
        for record in self:
            if record.state == 'register':
                record.state = 'registered'

    def queue_registered(self):
        for record in self:
            if record.state == 'registered':
                record.state = 'waiting_triage'

    def queue_waiting_triage(self):
        for record in self:
            if record.state == 'waiting_triage':
                record.state = 'triage'

    def queue_triage(self):
        for record in self:
            if record.state == 'triage':
                record.state = 'waiting_cons'

    def queue_waiting_cons(self):
        for record in self:
            if record.state == 'waiting_cons':
                record.state = 'consultation'

    def queue_consultation(self):
        for record in self:
            if record.state == 'consultation':
                record.state = 'waiting_payment'

    def queue_waiting_payment(self):
        for record in self:
            if record.state == 'waiting_payment':
                record.state = 'paying'

    def queue_paying(self):
        for record in self:
            if record.state == 'paying':
                record.state = 'done'

    def queue_cancel(self):
        for record in self:
            if record.state == 'cancel':
                record.state = 'register'

    class HrDepartment(models.Model):
        _inherit = 'hr.department'

        state_mapping = fields.Selection([
            ('register', 'Register'),
            ('registered', 'Registered'),
            ('waiting_triage', 'Waiting for Triage'),
            ('triage', 'Triage'),
            ('waiting_cons', 'Waiting for Consultation'),
            ('consultation', 'Consultation'),
            ('waiting_payment', 'Waiting for Payment'),
            ('paying', 'Payment in Progress'),
            ('cancel', 'Cancel'),
            ('done', 'Done'),
        ], string="State Mapping", help="This state will be applied to tokens in this department.")
