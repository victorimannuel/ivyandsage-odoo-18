from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class Delivery(WebsiteSale):
    
    @route('/website_sale/set_delivery_date', type='json', auth='public', website=True)
    def website_sale_set_pickup_location(self, date):
        order_sudo = request.website.sale_get_order()
        order_sudo._set_delivery_date(date)