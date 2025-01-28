import logging
from odoo import fields, models, _

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    square_environment = fields.Selection(
        selection=[
            ('sandbox', 'Sandbox'), 
            ('production', 'Production'), 
        ],
        string='Square Environment',
        default='sandbox',
        config_parameter='vt_odoo_square.square_environment',
    )
    square_application_id = fields.Char(
        string='Square Application ID',
        config_parameter='vt_odoo_square.square_application_id',
    )
    square_access_token = fields.Char(
        string='Square Access Token',
        config_parameter='vt_odoo_square.square_access_token',
    )
    square_location_id = fields.Char(
        string='Square Location ID',
        config_parameter='vt_odoo_square.square_location_id',
    )
    square_application_id_sandbox = fields.Char(
        string='Square Sandbox Application ID',
        config_parameter='vt_odoo_square.square_application_id_sandbox',
    )
    square_access_token_sandbox = fields.Char(
        string='Square Sandbox Access Token',
        config_parameter='vt_odoo_square.square_access_token_sandbox',
    )
    square_location_id_sandbox = fields.Char(
        string='Square Sandbox Location ID',
        config_parameter='vt_odoo_square.square_location_id_sandbox',
    )