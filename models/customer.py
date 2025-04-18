from odoo import models,fields,api
class BeautySalonCustomer(models.Model):
    _name = 'beauty.customer'
    _description = 'Beauty Salon Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    notes = fields.Text(string='Notes')

    # Relationships
    appointment_ids = fields.One2many('beauty.appointment', 'customer_id', string='Appointments')
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Appointment Count')

    # New computed field to fetch the packages a customer has acquired
    package_ids = fields.Many2many('beauty.package', compute='_compute_package_ids', string='Packages')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for customer in self:
            customer.appointment_count = len(customer.appointment_ids)

    @api.depends('appointment_ids.package_id')
    def _compute_package_ids(self):
        for customer in self:
            # Collecting distinct package ids from the customer's appointments
            packages = customer.appointment_ids.mapped('package_id')
            customer.package_ids = packages

    def action_view_appointments(self):
        self.ensure_one()
        action = self.env.ref('beauty_salon.action_beauty_appointment').read()[0]
        action['domain'] = [('customer_id', '=', self.id)]
        action['context'] = {'default_customer_id': self.id}
        return action