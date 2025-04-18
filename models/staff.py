# models/staff.py
from odoo import models, fields, api


class BeautySalonStaff(models.Model):
    _name = 'beauty.staff'
    _description = 'Beauty Salon Staff'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    position = fields.Selection([('junior assistant','Junior Assistant'),('senior assistant','Senior Assistant'),('owner','Owner')], string="Position")

    # Relationships
    service_ids = fields.Many2many('beauty.service', string='Services Provided')
    appointment_ids = fields.One2many('beauty.appointment', 'staff_id', string='Appointments')

    # Statistics
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Appointment Count')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for staff in self:
            staff.appointment_count = len(staff.appointment_ids)

    def action_view_appointments(self):
        self.ensure_one()
        action = self.env.ref('beauty_salon.action_beauty_appointment').read()[0]
        action['domain'] = [('staff_id', '=', self.id)]
        action['context'] = {'default_staff_id': self.id}
        return action
