import base64
import requests
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    faire_product_id = fields.Char(string='Faire Product ID')
    faire_variant_id = fields.Char(string='Faire Variant ID')
    faire_product_image_url = fields.Char(string='Faire Product Image URL')
    
    @api.onchange('faire_product_image_url')
    def _onchange_faire_product_image_url(self):
        if self.faire_product_image_url:
            try:
                response = requests.get(self.faire_product_image_url, timeout=10)
                if response.status_code == 200:
                    self.image_1920 = base64.b64encode(response.content)
            except Exception:
                self.image_1920 = False
        else:
            self.image_1920 = False