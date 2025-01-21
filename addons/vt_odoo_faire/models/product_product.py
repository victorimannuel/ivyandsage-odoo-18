import base64
import requests
from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    faire_product_id = fields.Char(string='Faire Product ID')
    faire_variant_id = fields.Char(string='Faire Variant ID')
    faire_product_image_url = fields.Char(string='Faire Product Image URL')
    retail_price = fields.Float(string='Retail Price')
    wholesale_price = fields.Float(string='Wholesale Price')
    min_qty = fields.Integer(string='Minimum Quantity')
    
    # @api.onchange('wholesale_price')
    # def _onchange_wholesale_price(self):
    #     self.lst_price = self.wholesale_price
        
    def _process_faire_product_image_url(self):
        for record in self:
            url = record.faire_product_image_url
            if url:
                try:
                    response = requests.get(url, timeout=20)
                    if response.status_code == 200:
                        record.image_1920 = base64.b64encode(response.content)
                except Exception:
                    record.image_1920 = False