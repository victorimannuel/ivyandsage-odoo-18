import json
import logging
import requests
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FaireAuthController(http.Controller):

    @http.route('/faire/oauth2/authorization-callback', auth='none')
    def oauth_callback(self, **kwargs):
        """Handles the OAuth callback and retrieves the authorization code."""
        
        _logger.info("OAuth callback accessed with params: %s", kwargs)
        authorization_code = kwargs.get('authorization_code')
        state = kwargs.get('state')
        
        faire = request.env['faire.oauth'].sudo().search([('active', '=', True), ('state', '=', state)], limit=1)
        _logger.info("Faire oAuth record: %s", faire)
        if authorization_code and faire:
            faire.sudo().write({
                'authorization_code': authorization_code
            })
            
            access_token_data = self.get_access_token(faire.application_id, faire.secret_id, faire.redirect_url, faire.scope_ids, authorization_code)
            if access_token_data:
                faire.sudo().write({
                    'oauth_access_token': access_token_data.get('accessToken'),
                    'token_type': access_token_data.get('tokenType'),
                    'status': 'active',
                })
                
        return request.redirect('/faire/oauth2/success')
    
    
    def get_access_token(self, application_id, secret_id, redirect_url, scope_ids, authorization_code):
        """Retrieve access token using authorization code."""
        token_url = "https://www.faire.com/api/external-api-oauth2/token"
        
        payload = {
            "application_token": application_id,
            "application_secret": secret_id,
            "redirect_url": redirect_url,
            "scope": [scope.name for scope in scope_ids],
            "grant_type": "AUTHORIZATION_CODE",
            "authorization_code": authorization_code,
        }
        
        _logger.info("Access token payload: %s", payload)
        response = requests.post(token_url, json=payload)
        _logger.info("Access token response: %s", response)
        if response.status_code == 200:
            return response.json()  # Returns access token data
        else:
            # Handle errors (log the error or raise an exception)
            return None
        
        
    @http.route('/faire/oauth2/success', auth='public', methods=['GET'], csrf=False)
    def success_page(self, **kwargs):
        """Render the success page after successful authorization."""
        return request.render('vt_odoo_faire.success_page_template', {})
