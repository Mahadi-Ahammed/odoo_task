from odoo import models, fields, api

class PropertyStage(models.Model):
    _name = 'property.stage'
    _description = 'Property Stage'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(string="Stage Name", required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer(string="Sequence", default=10)
    color = fields.Integer(string="Color Index")
    fold = fields.Boolean(string="Folded in Kanban")
