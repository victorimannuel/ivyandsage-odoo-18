import base64
import requests
from odoo import api, fields, models, _
from odoo.http import request
import requests


class FaireAPIService(models.Model):
    _name = "faire.api.service"
    _description = "Faire API Service"
    
    name = fields.Char(string='Name')

    # Your string to encode
    credentials = "{}:{}"

    # Encode the string
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    def get_all_orders(self):
        """Get all orders."""
        self.ensure_one()
        headers = {
            'X-FAIRE-APP-CREDENTIALS': 'YXBhX2p3cHc1ZTN0ZGU6OWx3dzZxdDFmMm10ZzRuZ3owMjV4OGlweWF4ZjM3aDV1dTd6cnpnNDk2bGNjYnFzd3ozcTY4d2hwcWJncXo3djltYTNubzQ0b3ZrYmIyaWpzdmdoNGcwZ3dkam40YWUydmkzcQ==',
            'X-FAIRE-OAUTH-ACCESS-TOKEN': 'oaa_c34xjgtf2zz8kr6u3sjphf7gc4nb2v2if8w4s4k1ste26lqd7bd2xxl8kvh658rdemwz4pvh81ralbvvnacjjyekx7h6gz35'
        }
        
        url = "https://www.faire.com/external-api/v2/orders"
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")