from odoo import models, fields, api
from odoo.exceptions import UserError


class MyCustom(models.Model):
    _name = 'my.custom'
    _description = 'My Custom Model'

    name = fields.Char(string='Name', required=True)
    latitude = fields.Float(string='Latitude', digits=(10, 7))
    longitude = fields.Float(string='Longitude', digits=(10, 7))
    address = fields.Char(string='Address')
    openstreetmap_url = fields.Char(string='OpenStreetMap URL', compute='_compute_openstreetmap_url', store=True)

    @api.depends('latitude', 'longitude')
    def _compute_openstreetmap_url(self):
        for record in self:
            record.openstreetmap_url = f"https://www.openstreetmap.org/export/embed.html?bbox={record.longitude-0.01},{record.latitude-0.01},{record.longitude+0.01},{record.latitude+0.01}&layer=mapnik&marker={record.latitude},{record.longitude}"
