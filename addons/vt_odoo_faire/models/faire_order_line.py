from odoo import api, fields, models, _


class FaireOrderLine(models.Model):
    _name = "faire.order.line"
    _description = "Faire Order Line"
    
    order_id = fields.Many2one(comodel_name='faire.order')
    faire_order_id = fields.Char(string='Faire Order ID')
    faire_order_line_id = fields.Char(string='Faire Order Line ID')
    created_at = fields.Datetime(string='Created At')
    updated_at = fields.Datetime(string='Updated At')
    # product_id = fields.Many2one(comodel_name='faire.product')
    # product_variant_id = fields.Many2one(comodel_name='faire.product.variant')
    quantity = fields.Integer(string='Quantity')
    price_cents = fields.Float(string='Price Cents')
    # product_name = fields.Many2one(comodel_name='faire.product', related='product_id.name')
    # product_variant_name = fields.Many2one(comodel_name='faire.product.variant', related='product_variant_id.name')
    product_name = fields.Char(string='Product Name')
    product_variant_name = fields.Char(string='Product Variant Name')
    includes_tester = fields.Boolean(string='Includes Tester')
    # price = 
    state = fields.Char(string='State')
    # customizations
    # discounts
    
    # 'items': [{'id': 'oi_f5h3dyu4t6', 'created_at': '2023-08-30T18:22:10.000Z', 'updated_at': '2023-09-29T08:33:05.000Z', 'order_id': 'bo_fhqq7dzfum', 'product_id': 'p_8w4k4wyaas', 'variant_id': 'po_rdk3tuqcqk', 'quantity': 7, 'price_cents': 650, 'product_name': 'Car Diffuser: Sexy Sandlewood', 'variant_name': 'default', 
            #    'includes_tester': False, 'price': {...}, 'state': 'DELIVERED', 'customizations': [...], 'discounts': [...]}, {'id': 'oi_qjgynxgat2', 'created_at': '2023-08-30T18:22:10.000Z', 'updated_at': '2023-09-29T08:33:05.000Z', 'order_id': 'bo_fhqq7dzfum', 'product_id': 'p_5wk2qdnye5', 'variant_id': 'po_9b6e8qr5uy', 'quantity': 7, 'price_cents': 650, 'product_name': 'Car Diffuser: Newport', 'variant_name': 'default', 'includes_tester': False, 'price': {...}, 'state': 'DELIVERED', 'customizations': [...], 'discounts': [...]}]

