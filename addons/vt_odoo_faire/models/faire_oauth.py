import base64
import logging
import pytz
import random
import requests
import string
from datetime import datetime
from odoo import fields, models, _

_logger = logging.getLogger(__name__)


def generate_random_state():
    # Generate a random string of length 10
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Faire(models.Model):
    _name = "faire.oauth"
    _description = "Faire OAuth"
    
    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name")
    date_request = fields.Datetime(string='Request Date', readonly=True)
    application_id = fields.Char(string='Application ID')
    secret_id = fields.Char(string='Secret ID')
    scope_ids = fields.Many2many(comodel_name='faire.permission.scope', string='Permission Scope')
    state = fields.Char(string="State (CSRF)", default=generate_random_state(), readonly=True)
    status = fields.Selection([
        ('idle', 'Idle'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ], default='idle')
    redirect_url = fields.Char(string="Redirect URL", readonly=True)
    authorization_url = fields.Char(string="Authorization URL", readonly=True)
    authorization_code = fields.Char(string="Authorization Code", readonly=True)
    oauth_access_token = fields.Char(string="OAuth Access Token", readonly=True)
    token_type = fields.Char(string="Token Type", readonly=True)
    
    
    def button_authorize(self):
        """Generate the authorization URL and update the state."""
        self.ensure_one()
        
        # Prepare data
        application_id = self.application_id
        scope = [scope.name for scope in self.scope_ids]
        state = generate_random_state()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = f'{base_url}/faire/oauth2/authorization-callback'
        self.redirect_url = redirect_url
        auth_url = f"https://faire.com/oauth2/authorize?applicationId={application_id}&scope={','.join(scope)}&state={state}&redirectUrl={redirect_url}"
        
        # Update fields
        self.state = state
        self.authorization_url = auth_url
        self.date_request = fields.Datetime.now()
        
        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }
        
    def button_authenticate(self):
        """Retrieve access token using authorization code."""
        token_url = "https://www.faire.com/api/external-api-oauth2/token"
        
        # Prepare the payload
        payload = {
            "application_token": self.application_id,
            "application_secret": self.secret_id,
            "redirect_url": self.redirect_url,
            "scope": [scope.name for scope in self.scope_ids],
            "grant_type": "AUTHORIZATION_CODE",
            "authorization_code": self.authorization_code,
        }

        _logger.info("Access token payload: %s", payload)

        # Send POST request using form-urlencoded
        # headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # response = requests.post(token_url, data=payload, headers=headers)
        
        # Send POST request using json
        headers = {"Content-Type": "application/json"}
        response = requests.post(token_url, json=payload, headers=headers)

        # Log the response content for debugging
        _logger.info("Access token response: %s", response.text)

        if response.status_code == 200:
            json_response = response.json()
            self.write({
                'oauth_access_token': json_response.get('accessToken'),
                'token_type': json_response.get('tokenType'),
                'status': 'active',
            })
        else:
            # Log the detailed error for debugging purposes
            _logger.error("Error retrieving access token: %s", response.text)
            return None
        
    def convert_to_timezone(self, user_timezone, utc_time_str):
        """
        Convert a UTC time string to a given timezone.
        
        :param utc_time_str: UTC time in string format (e.g., '2023-08-30T01:26:07.000Z')
        :param user_timezone: The desired timezone (e.g., 'Asia/Jakarta')
        :return: The converted time as a string in the desired timezone.
        """
        # Parse the UTC time
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%S.000Z')
        # Localize the UTC time
        utc_time = pytz.utc.localize(utc_time)
        # Convert to the desired timezone
        timezone = pytz.timezone(user_timezone)
        local_time = utc_time.astimezone(timezone)
        
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
        
    def get_all_orders(self):
        """Get all orders."""
        self.ensure_one()
        
        page = 1
        all_orders = []
        
        credentials = f'{self.application_id}:{self.secret_id}'
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        
        headers = {
            'X-FAIRE-APP-CREDENTIALS': encoded_credentials,
            'X-FAIRE-OAUTH-ACCESS-TOKEN': self.oauth_access_token
        }
        
        url = "https://www.faire.com/external-api/v2/orders"
        response = requests.get(url, headers=headers)
        while True:
            # Fetch orders for the current page
            response = requests.get(f"{url}?page={page}", headers=headers)
            if response.status_code == 200:
                orders = response.json().get('orders')
                if not orders:  # No more orders to fetch
                    break
                all_orders.extend(orders)
                page += 1  # Move to the next page
            else:
                print(f"Error fetching orders: {response.status_code}")
                break
            
        for order in all_orders:
            user_tz = self.env.user.tz
            order_id = order['id']
            
            faire_order = self.env['faire.order'].search(
                domain=[('faire_order_id', '=', order_id)]
            )
            # Order Lines
            order_line_ids = []
            existing_order_line_ids = []
            if faire_order:
                existing_order_line_ids = {line.faire_order_line_id: line.id for line in faire_order.order_line_ids}
                
            for item in order['items']:
                line_values = {
                    'faire_order_id': item['order_id'],
                    'faire_order_line_id': item['id'],
                    'created_at': self.convert_to_timezone(user_tz, item['created_at']),
                    'updated_at': self.convert_to_timezone(user_tz, item['updated_at']),
                    'quantity': item['quantity'],
                    'price_cents': item['price_cents'],
                    'product_name': item['product_name'],
                    'product_variant_name': item['variant_name'],
                    'includes_tester': item['includes_tester'],
                    'state': item['state'],
                }
                
                # To determine wether to create or update
                # Append to order_line_ids with the correct command
                if item['id'] in existing_order_line_ids:
                    order_line_ids.append((1, existing_order_line_ids[item['id']], line_values))  # Update if exists
                else:
                    order_line_ids.append((0, 0, line_values))  # Create if new
                
            values = {
                'display_id': order['display_id'],
                'created_at': self.convert_to_timezone(user_tz, order['created_at']),
                'updated_at': self.convert_to_timezone(user_tz, order['updated_at']),
                'state': order['state'],
                'customer_name': order['customer'].get('first_name') + ' ' + order['customer'].get('last_name'),
                # 'address': order['address'],
                'ship_after': self.convert_to_timezone(user_tz, order['ship_after']),
                # 'payout_costs': order['payout_costs'],
                'payment_initiated_at': self.convert_to_timezone(user_tz, order['payment_initiated_at']) if order.get('payment_initiated_at') else False,
                'retailer_id': order['retailer_id'],
                'source': order['source'],
                'expected_ship_date': self.convert_to_timezone(user_tz, order['expected_ship_date']) if order.get('expected_ship_date') else False,
                # 'customer': order['customer'],
                'processing_at': self.convert_to_timezone(user_tz, order['processing_at']) if order.get('processing_at') else False,
                'is_free_shipping': order['is_free_shipping'],
                'free_shipping_reason': order['free_shipping_reason'] if order['is_free_shipping'] == True else '',
                # 'faire_covered_shipping_cost': order['faire_covered_shipping_cost'],
                'order_line_ids': order_line_ids,
                # 'shipments': order['shipments'],
                # 'brand_discount': order['brand_discount'],
            }
            
            if len(faire_order) == 0:
                values.update({'faire_order_id': order_id})
                self.env['faire.order'].create(values)
            else:
                faire_order.write(values)
        
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {response.json()}")