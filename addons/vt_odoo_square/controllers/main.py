import json
import logging
from odoo import http
from odoo.http import request, route, Controller

_logger = logging.getLogger(__name__)


class SquareController(http.Controller):

    @http.route("/square/tokenize-card", auth="none")
    def tokenize_card(self, **kwargs):
        # Render the card HTML template
        return request.render("vt_odoo_square.square_card_view_template")
    
    @route('/square/get_square_credentials', auth='user', type='json', methods=['POST'])
    def get_square_credentials(self):
        # Ensure only authorized users can fetch the credentials
        if not request.env.user.has_group('base.group_user'):
            return {"error": "Unauthorized"}
        
        square_environment = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_environment')
        if square_environment == 'sandbox':
            app_id = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_application_id_sandbox')
            location_id = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_location_id_sandbox')
        elif square_environment == 'production':
            app_id = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_application_id')
            location_id = request.env['ir.config_parameter'].get_param('vt_odoo_square.square_location_id')
        
        return {
            'appId': app_id,
            'locationId': location_id,
        }
        
    @http.route('/square/set_card_information', auth='user', type='http', methods=['POST'], csrf=False)
    def set_square_information(self, **kwargs):
        # Ensure only authorized users can fetch the appId
        if not request.env.user.has_group('base.group_user'):
            return {"error": "Unauthorized"}
        
        raw_data = request.httprequest.data
        data = json.loads(raw_data)
        print('heeeeeeeeeeeeeeeeeee', self, data)
        
        order_id = data.get('order_id')
        card_nonce = data.get('card_nonce')
        card_information_json = data.get('card_information_json')
        
        try:
            sale_order = request.env['sale.order'].search([('id', '=', order_id)])
            sale_order.square_card_nonce = card_nonce
            sale_order.square_card_information_json = card_information_json
            return http.Response(status=200)
        except Exception:
            return http.Response(status=400)
            
        
    @http.route('/my_component', auth='user', website=True)
    def render_my_component(self, **kw):
        return request.render('vt_odoo_square.my_component_template')
