from odoo import models, fields

class PropertyImage(models.Model):
    _name = 'property.image'
    _description = 'Property Images'

    name = fields.Char(string="Image Name")
    image = fields.Binary(string="Image", required=True)
    property_id = fields.Many2one('bay.vista.property', string="Property")
