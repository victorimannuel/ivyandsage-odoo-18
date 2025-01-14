from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    faire_product_id = fields.Char(string='Faire Product ID')
    faire_variant_id = fields.Char(string='Faire Variant ID')