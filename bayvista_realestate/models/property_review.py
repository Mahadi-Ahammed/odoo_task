from odoo import models, fields

class PropertyReview(models.Model):
    _name = 'property.review'
    _description = 'Property Review'
    
    property_id = fields.Many2one('bay.vista.property', string='Property', required=True, ondelete='cascade')
    property_user_id = fields.Many2one('bay.vista.user', string='Reviewed By', required=True)
    comment = fields.Text(string='Comment', required=True)
    rating = fields.Integer(string='Rating', help="Rating between 1 and 5", default=0)
