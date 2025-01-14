from odoo import api, fields, models, _


class FaireProduct(models.Model):
    _name = "faire.product"
    _description = "Faire Product"
    
    name = fields.Char(string='Name')
    faire_product_id = fields.Char(string='Faire Product ID')
    display_id = fields.Char(string='Faire Display ID')
    created_at = fields.Datetime(string='Created At')
    updated_at = fields.Datetime(string='Updated At')
    state = fields.Selection(selection=[
        'NEW', 'The order has not yet been accepted by the brand.'
        'PROCESSING', 'The brand has accepted the order, and is in the process of fulfilling it.'
        'PRE_TRANSIT', 'The order has at least one shipment, but no shipments are in transit.'
        'IN_TRANSIT', 'At least one of the shipments is in transit.'
        'DELIVERED', 'At least one of the shipments has been delivered.'
        'PENDING_RETAILER_CONFIRMATION', 'The brand did not have sufficient quantity to fulfill the order; the retailer needs to decide whether they want to wait till the items are back in stock, or cancel.'
        'BACKORDERED', 'The brand did not have sufficient quantity to fulfill the order and will ship it when items are back in stock.'
        'CANCELED',	'The order was canceled by the brand or the retailer.'
    ], string='State')
    address = fields.Many2one(comodel_name='faire.address')
    ship_after = fields.Datetime(string='Ship After')
    # payout_costs
    payment_initiated_at = fields.Datetime(string='Payment Initiated At')
    retailer_id = fields.Char(string='Retailer ID')
    source = fields.Char(string='Source')
    expected_ship_date = fields.Datetime(string='Expected Ship Date')
    # customer = fields.
    processing_at = fields.Datetime(string='Processing At')
    is_free_shipping = fields.Boolean(string='Is Free Shipping?')
    free_shipping_reason = fields.Char(string='Free Shipping Reason')
    # faire_covered_shipping_cost = fields.Json(string='Faire Covered Shipping Cost')
    item_ids = fields.Many2one(comodel_name='faire.product')
    
    # 'items': [{'id': 'oi_f5h3dyu4t6', 'created_at': '2023-08-30T18:22:10.000Z', 'updated_at': '2023-09-29T08:33:05.000Z', 'order_id': 'bo_fhqq7dzfum', 'product_id': 'p_8w4k4wyaas', 'variant_id': 'po_rdk3tuqcqk', 'quantity': 7, 'price_cents': 650, 'product_name': 'Car Diffuser: Sexy Sandlewood', 'variant_name': 'default', 'includes_tester': False, 'price': {...}, 'state': 'DELIVERED', 'customizations': [...], 'discounts': [...]}, {'id': 'oi_qjgynxgat2', 'created_at': '2023-08-30T18:22:10.000Z', 'updated_at': '2023-09-29T08:33:05.000Z', 'order_id': 'bo_fhqq7dzfum', 'product_id': 'p_5wk2qdnye5', 'variant_id': 'po_9b6e8qr5uy', 'quantity': 7, 'price_cents': 650, 'product_name': 'Car Diffuser: Newport', 'variant_name': 'default', 'includes_tester': False, 'price': {...}, 'state': 'DELIVERED', 'customizations': [...], 'discounts': [...]}]

