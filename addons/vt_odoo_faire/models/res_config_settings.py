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
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    faire_application_id = fields.Char(
        string='Faire Application ID',
        config_parameter='vt_odoo_faire.faire_application_id',
    )
    faire_application_secret_id = fields.Char(
        string='Faire Application Secret ID',
        config_parameter='vt_odoo_faire.faire_application_secret_id',
    )
    faire_api_state_code = fields.Char(
        string='Faire API State Code',
        config_parameter='vt_odoo_faire.faire_api_state_code',
        readonly=True,
    )
    faire_api_permission_scope = fields.Char(
        string='Faire API Permission Scope',
        config_parameter='vt_odoo_faire.faire_api_permission_scope',
    )
    faire_api_grant_type = fields.Char(
        string='Faire API Grant Type',
        config_parameter='vt_odoo_faire.faire_grant_type',
        default='AUTHORIZATION_CODE'
    )
    faire_api_redirect_url = fields.Char(
        string='Faire API Redirect URL',
        config_parameter='vt_odoo_faire.faire_api_redirect_url',
        default='/faire/oauth2/authorization-callback'
    )
    faire_authorization_code = fields.Char(
        string='Faire Authorization Code',
        config_parameter='vt_odoo_faire.faire_authorization_code',
        readonly=False
    )
    faire_oauth_access_token = fields.Char(
        string="Faire OAuth Access Token",
        config_parameter='vt_odoo_faire.faire_oauth_access_token',
        readonly=False
    )
    
    def faire_authorize(self):
        """Generate the authorization URL and update the state."""
        
        # Prepare data
        application_id = self.faire_application_id
        scope = self.faire_api_permission_scope.replace(',', '%20')
        state = generate_random_state()
        self.env['ir.config_parameter'].set_param('vt_odoo_faire.faire_api_state_code', state)
        redirect_url = self.faire_api_redirect_url
        
        auth_url = f"https://faire.com/oauth2/authorize?applicationId={application_id}&scope={scope}&state={state}&redirectUrl={redirect_url}"
        print('auth_url', auth_url)
        
        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }
        
    def faire_authenticate(self):
        """Retrieve access token using authorization code."""
        token_url = "https://www.faire.com/api/external-api-oauth2/token"
        
        # Prepare the payload
        payload = {
            "application_token": self.faire_application_id,
            "application_secret": self.faire_application_secret_id,
            "redirect_url": self.faire_api_redirect_url,
            "scope": self.faire_api_permission_scope.split(","),
            "grant_type": "AUTHORIZATION_CODE",
            "authorization_code": self.faire_authorization_code,
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
            self.env['ir.config_parameter'].set_param('vt_odoo_faire.faire_oauth_access_token', json_response.get('access_token'))
        else:
            # Log the detailed error for debugging purposes
            _logger.error("Error retrieving access token: %s", response.text)
            return None
        
    def faire_revoke(self):
        """Revoke access token."""
        url = "https://www.faire.com/api/external-api-oauth2/revoke"
        
        # Prepare the payload
        payload = {
            "application_token": self.faire_application_id,
            "application_secret": self.faire_application_secret_id,
            "access_token_o_auth": self.faire_oauth_access_token,
        }
        _logger.info("Revoke payload: %s", payload)
        
        # Send POST request using json
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        
        # Log the response content for debugging
        _logger.info("Revoke token response: %s", response.text)
        
        if response.status_code == 200:
            # self.env['ir.config_parameter'].set_param('vt_odoo_faire.faire_oauth_access_token', False)
            # Unlink the token record
            self.env['ir.config_parameter'].search([('key', '=', 'vt_odoo_faire.faire_oauth_access_token')]).unlink()
            self.env['ir.config_parameter'].search([('key', '=', 'vt_odoo_faire.faire_authorization_code')]).unlink()
        else:
            # Log the detailed error for debugging purposes
            _logger.error("Error revoking access token: %s", response.text)
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
    
    def convert_cents_to_dollars(self, cents):
        return cents / 100
        
    
    def faire_get_all_products(self):
        """Get all products."""
        self.ensure_one()
        
        page = 1
        all_products = []
        
        credentials = f'{self.faire_application_id}:{self.faire_application_secret_id}'
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        
        headers = {
            'X-FAIRE-APP-CREDENTIALS': encoded_credentials,
            'X-FAIRE-OAUTH-ACCESS-TOKEN': self.faire_oauth_access_token
        }
        
        url = "https://www.faire.com/external-api/v2/products"
        response = requests.get(url, headers=headers)
        while True:
            # Fetch products for the current page
            response = requests.get(f"{url}?page={page}", headers=headers)
            if response.status_code == 200:
                products = response.json().get('products')
                if not products:  # No more orders to fetch
                    break
                all_products.extend(products)
                page += 1  # Move to the next page
            else:
                print(f"Error fetching products: {response.status_code}")
                break
        
        # Creating a wholesale pricelist
        # wholesale_pricelist = self.env['product.pricelist'].create({
        #     'name': 'Wholesale Pricelist',
        # })
        
        # Updating default pricelist
        default_pricelist = self.env['product.pricelist'].search([('name', 'ilike', 'Default')], limit=1)
        website = self.env['website'].search([], limit=1)
        default_pricelist.website_id = website.id
        # NOTES: Make sure the website in the pricelist ecommerce tab is not empty,
        # otherwise the price in ecommerce (frontend) won't be using this wholesale pricelist
        
        # Creating product categories from Faire's taxonomies
        self.get_and_create_ecommerce_categories(headers)
        
        # Create product attributes
        self.get_and_create_variant_options(all_products)
        
        for product in all_products:
            # TODO: Currently only able to create new, not editing the existing
            product_template = self.env['product.template'].search(
                domain=[('faire_product_id', '=', product['id'])]
            )
            if not product_template:
                # Updating product variants value
                variants = []
                for option in product['variant_option_sets']:
                    variants.append({
                        'attribute': self.env['product.attribute'].search([('name', '=', option['name'])])
                    })
                for source_variant in product['variants']:
                    for variant in variants:
                        for option in source_variant['options']:
                            if option['name'] == variant['attribute'].name:
                                attribute = self.env['product.attribute'].search([('name', '=', option['name'])])
                                value = self.env['product.attribute.value'].search([
                                    ('attribute_id', '=', attribute.id),
                                    ('name', '=', option['value']),
                                ])
                                print(variant.get('values'))
                                variant.update({
                                    'values': value + variant['values'] if 'values' in variant else value,
                                    'price_extra': source_variant['wholesale_price_cents']
                                })
                
                # Creating new product template
                ecommerce_category = self.env['product.public.category'].search([('name', '=', product['taxonomy_type']['name'])])
                product_template = self.env['product.template'].create({
                    'faire_product_id': product['id'],
                    'name': product['name'],
                    'description': product['description'],
                    'faire_product_image_data': product['images'],
                    'min_qty': product['minimum_order_quantity'] or 0,
                    'description_ecommerce': product['description'],
                    'is_published': True,
                    'available_in_pos': True,
                    'public_categ_ids': ecommerce_category.ids,
                    'wholesale_price': self.convert_cents_to_dollars(source_variant['wholesale_price_cents'] or 0),
                    'retail_price': self.convert_cents_to_dollars(source_variant['retail_price_cents'] or 0),
                })
                
                # Creating new product variants through product.template.attribute.line model
                for variant in variants:
                    self.env['product.template.attribute.line'].create({
                        'product_tmpl_id': product_template.id,
                        'attribute_id': variant['attribute'].id,
                        'value_ids': variant['values'].ids,
                    })
                
                # Updating product variants value
                related_products = self.env['product.product'].search([
                    ('product_tmpl_id', '=', product_template.id),
                ])
                for related_product in related_products:
                    for source_variant in product['variants']:
                        if related_product.display_name.__contains__(source_variant['name']) or source_variant['name'] == 'default':
                            related_product.write({
                                'faire_product_id': product['id'],
                                'faire_variant_id': source_variant['id'],
                                'name': product['name'],
                                'description': product['description'],
                                'faire_product_image_data': source_variant['images'] if source_variant.get('images') else product['images'],
                                'qty_available': source_variant['available_quantity'] if source_variant.get('available_quantity') else 0,
                                # 'wholesale_price': variant['prices'][0]['wholesale_price']['amount_minor'] if variant.get('prices') else 0,
                                # 'retail_price': variant['prices'][0]['wholesale_price']['amount_minor'] if variant.get('prices') else 0,
                                'wholesale_price': self.convert_cents_to_dollars(source_variant['wholesale_price_cents'] or 0),
                                'retail_price': self.convert_cents_to_dollars(source_variant['retail_price_cents'] or 0),
                            })
                    
                    # Creating new pricelist item
                    self.env['product.pricelist.item'].create({
                        'pricelist_id': default_pricelist.id,
                        'display_applied_on': '1_product',
                        'product_tmpl_id': product_template.id,
                        'product_id': related_product.id,
                        'compute_price': 'fixed',
                        'fixed_price': related_product.wholesale_price,
                        'min_quantity': related_product.min_qty or 0,
                    })
                    
    def get_and_create_variant_options(self, products):
        variant_option_list = []
        for product in products:
            for option in product['variant_option_sets']:
                if option['name'] not in [option['name'] for option in variant_option_list]:
                    variant_option_list.append(option)
                else:
                    for target_option in variant_option_list:
                        if target_option['name'] == option['name']:
                            for value in option['values']:
                                if value not in target_option['values']:
                                    target_option['values'].append(value)
                                    target_option['values'] = sorted(target_option['values'])
        
        product_attributes = self.env['product.attribute'].search([])
        for option in variant_option_list:
            if option['name'] not in [attribute.name for attribute in product_attributes]:
                self.env['product.attribute'].create({
                    'name': option['name'],
                    'display_type': 'pills',
                    'value_ids': [(0, 0, {'name': value}) for value in option['values']]
                })
    
    def get_and_create_ecommerce_categories(self, headers):
        url = "https://www.faire.com/external-api/v2/products/types"
        taxonomies = requests.get(url, headers=headers)
        for taxonomy in taxonomies.json().get('taxonomy_types'):
            self.env['product.public.category'].create({
                # TODO: Create faire_id field if necessary
                # 'faire_id': taxonomy['id'],
                'name': taxonomy['name']
            })
    
    def faire_get_all_orders(self):
        """Get all orders."""
        # self.ensure_one()
        
        # These conditions are for cron jobs
        if not self:
            # Search for existing res.config.settings record
            self = self.env['res.config.settings'].sudo().search([], limit=1, order='id desc')
        if not self:
            # Create new res.config.settings record
            self = self.env['res.config.settings'].create({})
        
        page = 1
        all_orders = []
        
        credentials = f'{self.faire_application_id}:{self.faire_application_secret_id}'
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        
        headers = {
            'X-FAIRE-APP-CREDENTIALS': encoded_credentials,
            'X-FAIRE-OAUTH-ACCESS-TOKEN': self.faire_oauth_access_token
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
            user_tz = self.env.user.tz or 'UTC'
            order_id = order['id']
            
            faire_order = self.env['faire.order'].search(
                domain=[('faire_order_id', '=', order_id)]
            )
            # Order Lines
            order_line_ids = []
            existing_order_line_ids = []
            if faire_order:
                existing_order_line_ids = {line.faire_order_line_id: line.id for line in faire_order.order_line_ids}
                
            amount_total = 0
            for item in order['items']:
                line_values = {
                    'faire_order_id': item['order_id'],
                    'faire_order_line_id': item['id'],
                    'created_at': self.convert_to_timezone(user_tz, item['created_at']),
                    'updated_at': self.convert_to_timezone(user_tz, item['updated_at']),
                    'quantity': item['quantity'],
                    'price_cents': self.convert_cents_to_dollars(item['price_cents'] or 0),
                    'product_name': item['product_name'],
                    'product_variant_name': item['variant_name'],
                    'includes_tester': item['includes_tester'],
                    'state': item['state'],
                    'amount_subtotal': self.convert_cents_to_dollars(item['price_cents'] or 0) * item['quantity'],
                }
                amount_total += line_values['amount_subtotal']
                
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
                'amount_total': amount_total,
            }
            
            if len(faire_order) == 0:
                values.update({'faire_order_id': order_id})
                self.env['faire.order'].create(values)
            else:
                faire_order.write(values)
        
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {response.json()}")