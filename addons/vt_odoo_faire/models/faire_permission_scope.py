from odoo import api, fields, models, _


class FairePermissionScope(models.Model):
    _name = "faire.permission.scope"
    _description = "Faire Permission Scope"
    
    name = fields.Char(string="Name")
    description = fields.Char(string='Description')
    type = fields.Selection([
        ('read', 'Read'),
        ('write', 'Write'),
    ])
    
    