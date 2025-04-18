# models/package.py
from odoo import models, fields, api


class BeautySalonPackage(models.Model):
    _name = 'beauty.package'
    _description = 'Beauty Salon Package'

    name = fields.Char(string='Package Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Package Price', required=True)
    duration = fields.Float(string='Total Duration (hours)', compute='_compute_duration')
    active = fields.Boolean(default=True)
    category = fields.Char(string='Category')  # Adding category

    # Relationships
    service_ids = fields.Many2many('beauty.service', 'beauty_service_package_rel',
                                   'package_id', 'service_id', string='Services Included')

    @api.depends('service_ids')
    def _compute_duration(self):
        for package in self:
            package.duration = sum(service.duration for service in package.service_ids)

    @api.onchange('service_ids')
    def _onchange_service_ids(self):
        if not self.service_ids:
            return
        suggested_price = sum(service.price for service in self.service_ids)
        # Usually packages offer a discount
        self.price = suggested_price * 0.9