import base64
import requests
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    faire_product_id = fields.Char(string='Faire Product ID')
    faire_variant_id = fields.Char(string='Faire Variant ID') # Deprecated
    faire_product_image_url = fields.Char(string='Faire Product Image URL')
    faire_product_image_data = fields.Json(string='Faire Product Image Data')
    retail_price = fields.Float(string='Retail Price') # Deprecated
    wholesale_price = fields.Float(string='Wholesale Price') # Deprecated
    min_qty = fields.Integer(string='Minimum Quantity') # Deprecated
    
    def _process_faire_product_image_data(self):
        for record in self:
            for index, data in enumerate(record.faire_product_image_data):
                print(data)
                try:
                    response = requests.get(data['url'], timeout=20)
                    if response.status_code == 200:
                        image = base64.b64encode(response.content)
                        if index == 0:
                            record.image_1920 = image
                            
                        record.env['product.image'].create({
                            'product_tmpl_id': record.id,
                            'name': '- '.join(data['tags']),
                            'image_1920': image,
                        })
                        print('Image generated!')
                except Exception:
                    record.image_1920 = False
            
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         print(vals)
    #         if 'faire_product_image_url' in vals:
    #             self._process_faire_product_image_url(vals['faire_product_image_url'])
    #     return super().create(vals_list)
    
    # def write(self, vals):
    #     if 'faire_product_image_url' in vals:
    #         self._process_faire_product_image_url(vals['faire_product_image_url'])
    #     return super().write(vals)