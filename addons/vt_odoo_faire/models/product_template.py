import base64
import requests
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    faire_product_id = fields.Char(string='Faire Product ID')
    faire_variant_id = fields.Char(string='Faire Variant ID')
    faire_product_image_url = fields.Char(string='Faire Product Image URL')
    
    def _process_faire_product_image_url(self, url):
        if url:
            try:
                response = requests.get(url, timeout=20)
                if response.status_code == 200:
                    self.image_1920 = base64.b64encode(response.content)
            except Exception:
                self.image_1920 = False
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            print(vals)
            if 'faire_product_image_url' in vals:
                self._process_faire_product_image_url(vals['faire_product_image_url'])
        return super().create(vals_list)
    
    def write(self, vals):
        if 'faire_product_image_url' in vals:
            self._process_faire_product_image_url(vals['faire_product_image_url'])
        return super().write(vals)