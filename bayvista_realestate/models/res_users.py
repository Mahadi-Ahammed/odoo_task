
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Role field in Odoo's user model (syncs with BayVistaUser)
    role_sync = fields.Selection([
        ('buyer', 'Buyer'),
        ('owner', 'Owner'),
        ('admin', 'Admin'),
    ], string="User Role")