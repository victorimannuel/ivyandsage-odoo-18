import logging
import requests
import uuid
from odoo import fields, models, _
from odoo.http import request

_logger = logging.getLogger(__name__)

def generate_uuid():
    return str(uuid.uuid4())

def dollars_to_cents(dollars):
    return int(dollars * 100)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    square_card_nonce = fields.Char(
        string='Card Nonce',
        readonly=True
    )
    square_card_information_json = fields.Json(
        string='Card Information JSON',
        readonly=True
    )
    square_customer_id = fields.Char(
        string='Customer ID',
        readonly=True
    )
    square_card_id = fields.Char(
        string='Card ID',
        readonly=True
    )
    # square_card_idempotency_key = fields.Char(
    #     string='Card Idempotency Key',
    #     readonly=True
    # )
    # square_payment_idempotency_key = fields.Char(
    #     string='Payment Idempotency Key',
    #     readonly=True
    # )
    square_payment_id = fields.Char(
        string='Payment ID',
        readonly=True
    )
    square_payment_information_json = fields.Json(
        string='Square Payment Information JSON',
        readonly=True
    )
    
    def tokenize_card(self):
        params = {
            'order_id': self.id,
        }
        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = f'{base_url}/square/tokenize-card'
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        full_url = f"{url}?{query_string}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': full_url,
            'target': 'self',
        }
    
    def create_square_customer(self):
        square_environment = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_environment')
        endpoint = ''
        access_token = ''
        if square_environment == 'sandbox':
            endpoint = "https://connect.squareupsandbox.com/v2/customers"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token_sandbox')
        elif square_environment == 'production':
            endpoint = "https://connect.squareup.com/v2/customers"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token')
        
        # Prepare the payload
        payload = {
            "email_address": self.partner_id.email,
            "family_name": self.partner_id.name
        }
        
        _logger.info("Payload: %s", payload)
        
        # Check if exist
        customer = self.search_square_customer(payload['email_address'])
        if customer:
            self.square_customer_id = customer
            return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'success',
                        'sticky': False,
                        'message': _("Customer is already in Square!"),
                        'next': {'type': 'ir.actions.act_window_close'},
                    }
                }
        else:
            # Send POST request using json
            headers = {
                'Square-Version': '2025-01-23',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, json=payload, headers=headers)
            
            _logger.info("Response: %s", response.text)
            
            if response.status_code == 200:
                json_response = response.json()
                self.square_customer_id = json_response['customer']['id']
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'success',
                        'sticky': False,
                        'message': _("Successfully Created Customer in Square!"),
                        'next': {'type': 'ir.actions.act_window_close'},
                    }
                }
            else:
                # Log the detailed error for debugging purposes
                _logger.error("Error retrieving access token: %s", response.text)
                return None
        
    def search_square_customer(self, email_address):
        square_environment = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_environment')
        endpoint = ''
        access_token = ''
        if square_environment == 'sandbox':
            endpoint = "https://connect.squareupsandbox.com/v2/customers/search"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token_sandbox')
        elif square_environment == 'production':
            endpoint = "https://connect.squareup.com/v2/customers/search"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token')
        
        # Prepare the payload
        payload = {
            "query": {
                "filter": {
                    "email_address": {
                        "exact": email_address
                    }
                }
            }
        }
        
        _logger.info("Payload: %s", payload)
        
        # Send POST request using json
        headers = {
            'Square-Version': '2025-01-23',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        
        _logger.info("Response: %s", response.text)
        
        if response.status_code == 200:
            json_response = response.json()
            if 'customers' in json_response:
                customer_id = json_response['customers'][0]['id']
            else:
                customer_id = False
            
            return customer_id
        else:
            # Log the detailed error for debugging purposes
            _logger.error("Error retrieving access token: %s", response.text)
            return None
        
    def create_square_card(self):
        square_environment = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_environment')
        endpoint = ''
        access_token = ''
        if square_environment == 'sandbox':
            endpoint = "https://connect.squareupsandbox.com/v2/cards"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token_sandbox')
        elif square_environment == 'production':
            endpoint = "https://connect.squareup.com/v2/cards"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token')
        
        # Prepare the payload
        card_information = self.square_card_information_json
        payload = {
            "card": {
                "customer_id": self.square_customer_id,
                "cardholder_name": self.partner_id.name,
                "exp_month": card_information['details']['card']['expMonth'],
                "exp_year": card_information['details']['card']['expYear'],
            },
            "idempotency_key": generate_uuid(),
            "source_id": self.square_card_nonce
        }
        
        _logger.info("Payload: %s", payload)
        
        # Send POST request using json
        headers = {
            'Square-Version': '2025-01-23',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        
        _logger.info("Response: %s", response.text)
        
        if response.status_code == 200:
            json_response = response.json()
            self.square_card_id = json_response['card']['id']
        else:
            # Log the detailed error for debugging purposes
            _logger.error("Error retrieving access token: %s", response.text)
            return None
        
    def create_square_payment(self):
        square_environment = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_environment')
        endpoint = ''
        access_token = ''
        if square_environment == 'sandbox':
            endpoint = "https://connect.squareupsandbox.com/v2/payments"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token_sandbox')
        elif square_environment == 'production':
            endpoint = "https://connect.squareup.com/v2/cards"
            access_token = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_access_token')
        
        # Prepare the payload
        payload = {
            "idempotency_key": generate_uuid(),
            "source_id": self.square_card_id,
            "amount_money": {
                "amount": dollars_to_cents(self.amount_total),
                "currency": "USD"
            },
            "customer_id": self.square_customer_id,
        }
        _logger.info("Payload: %s", payload)
        
        # Send POST request using json
        headers = {
            'Square-Version': '2025-01-23',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        
        _logger.info("Response: %s", response.text)
        
        if response.status_code == 200:
            json_response = response.json()
            self.square_payment_id = json_response['payment']['id']
            self.square_payment_information_json = json_response
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'sticky': False,
                    'message': _("Successfully charged payment in Square!"),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        else:
            # Log the detailed error for debugging purposes
            _logger.error("Error retrieving access token: %s", response.text)
            return None
    
    def reset_square_information(self):
        self.square_card_nonce = False
        self.square_card_information_json = False
        self.square_customer_id = False
        self.square_card_id = False
        self.square_payment_id = False
        self.square_payment_information_json = False