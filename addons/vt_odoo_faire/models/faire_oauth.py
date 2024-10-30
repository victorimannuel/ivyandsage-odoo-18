import random
import string
from odoo import api, fields, models, _


def generate_random_state():
    # Generate a random string of length 10
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Faire(models.Model):
    _name = "faire.oauth"
    _desc = "Faire OAuth"
    
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
    authorization_url = fields.Char(string="Authorization URL", readonly=True)
    authorization_code = fields.Char(string="Authorization Code", readonly=True)
    oauth_access_token = fields.Char(string="OAuth Access Token", readonly=True)
    
    
    def button_authorize(self):
        """Generate the authorization URL and update the state."""
        self.ensure_one()
        
        # Prepare data
        application_id = self.application_id
        scope = [scope.name for scope in self.scope_ids]
        state = generate_random_state()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = f'{base_url}/faire/oauth2/authorization-callback'
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
        
        