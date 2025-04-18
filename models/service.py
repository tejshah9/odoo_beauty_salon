# models/service.py
from odoo import models, fields, api


class BeautySalonService(models.Model):
    _name = 'beauty.service'
    _description = 'Beauty Salon Service'

    name = fields.Char(string='Service Name', required=True)
    description = fields.Text(string='Description')
    duration = fields.Float(string='Duration (hours)', default=1.0)
    price = fields.Float(string='Price', required=True)
    category = fields.Selection([
        ('hair', 'Hair'),
        ('face', 'Face'),
        ('nails', 'Nails'),
        ('body', 'Body'),
        ('other', 'Other'),
    ], string='Category', required=True)
    active = fields.Boolean(default=True)

    # Relationships
    package_ids = fields.Many2many('beauty.package', 'beauty_service_package_rel',
                                   'service_id', 'package_id', string='Included in Packages')