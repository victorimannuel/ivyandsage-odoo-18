import random
import string
import logging
import requests
from odoo import api, fields, models, _
from odoo.http import request

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
            "applicationId": self.application_id,
            "applicationSecret": self.secret_id,
            "redirectUrl": self.redirect_url,  # Ensure this URL matches the registered one exactly
            # "scope": " ".join([scope.name for scope in self.scope_ids]),  # Ensure scope format is correct
            "scope": [scope.name for scope in self.scope_ids],  # Ensure scope format is correct
            "grantType": "AUTHORIZATION_CODE",  # Ensure this matches the required value
            "authorizationCode": self.authorization_code,  # Ensure this code is valid
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