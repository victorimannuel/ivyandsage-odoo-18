from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    retail_price = fields.Float(
        related='product_id.retail_price',
        string='Retail Price'
    )
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_uom_qty = self.product_id.product_tmpl_id.min_qty
        self.price_unit = self.product_id.wholesale_price
        
    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        self.price_unit = self.product_id.wholesale_price