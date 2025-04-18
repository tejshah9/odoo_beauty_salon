from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class BeautySalonAppointment(models.Model):
    _name = 'beauty.appointment'
    _description = 'Beauty Salon Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Appointment Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    date_start = fields.Datetime(string='Start Time', required=True, tracking=True)
    date_end = fields.Datetime(string='End Time', compute='_compute_date_end', store=True)
    duration = fields.Float(string='Duration (hours)', compute='_compute_duration')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancelled', 'Cancelled')],
                             string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    # Add category field
    category = fields.Char(string='Category')
    price = fields.Float(string='Price')

    # Relationships
    customer_id = fields.Many2one('beauty.customer', string='Customer', required=True)
    staff_id = fields.Many2one('beauty.staff', string='Staff Member', required=True)
    service_ids = fields.Many2many('beauty.service', string='Services')
    package_id = fields.Many2one('beauty.package', string='Package')

    # Financial
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, list):  # Handle list of vals correctly
            for val in vals:
                if val.get('name', _('New')) == _('New'):
                    val['name'] = self.env['ir.sequence'].next_by_code('beauty.appointment') or _('New')
            return super(BeautySalonAppointment, self).create(vals)
        else:  # Handle single dictionary case
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('beauty.appointment') or _('New')
            return super(BeautySalonAppointment, self).create(vals)

    @api.depends('service_ids', 'package_id')
    def _compute_total_price(self):
        for appointment in self:
            if appointment.package_id:
                appointment.total_price = appointment.package_id.price
            else:
                appointment.total_price = sum(service.price for service in appointment.service_ids)

    @api.depends('service_ids', 'package_id', 'date_start')
    def _compute_date_end(self):
        for appointment in self:
            if not appointment.date_start:
                appointment.date_end = False
                continue

            duration_hours = 0
            if appointment.package_id:
                duration_hours = appointment.package_id.duration
            else:
                duration_hours = sum(service.duration for service in appointment.service_ids)

            if duration_hours <= 0:
                duration_hours = 1  # Default to 1 hour

            hours = int(duration_hours)
            minutes = int((duration_hours - hours) * 60)
            appointment.date_end = appointment.date_start + timedelta(hours=hours, minutes=minutes)

    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for appointment in self:
            if appointment.date_start and appointment.date_end:
                delta = appointment.date_end - appointment.date_start
                appointment.duration = delta.total_seconds() / 3600
            else:
                appointment.duration = 0

    @api.onchange('package_id')
    def _onchange_package_id(self):
        if self.package_id:
            self.service_ids = [(6, 0, self.package_id.service_ids.ids)]

    @api.constrains('date_start', 'date_end', 'staff_id')
    def _check_staff_availability(self):
        for appointment in self:
            if appointment.date_start and appointment.date_end and appointment.staff_id:
                domain = [
                    ('id', '!=', appointment.id),
                    ('staff_id', '=', appointment.staff_id.id),
                    ('state', 'not in', ['cancelled']),
                    '|',
                    '&', ('date_start', '<=', appointment.date_start), ('date_end', '>', appointment.date_start),
                    '&', ('date_start', '<', appointment.date_end), ('date_end', '>=', appointment.date_end)
                ]
                overlapping = self.search_count(domain)
                if overlapping:
                    raise ValidationError(_("The staff member is already booked during this time slot!"))

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        return True

    def action_done(self):
        self.write({'state': 'done'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        return True

    def action_reset(self):
        self.write({'state': 'draft'})
        return True
