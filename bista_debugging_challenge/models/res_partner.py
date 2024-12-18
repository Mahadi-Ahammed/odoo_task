from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_area_manager = fields.Boolean(string='Is Area Manager')
    