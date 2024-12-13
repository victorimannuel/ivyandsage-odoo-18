import base64
import requests
from lxml import etree
from odoo import api, fields, models, _
from odoo.http import request
import requests


class FaireOrder(models.Model):
    _name = "faire.order"
    _description = "Faire Order"
    _order = "created_at desc"
    
    
    faire_order_id = fields.Char(string='Faire Order ID')
    display_id = fields.Char(string='Faire Display ID')
    created_at = fields.Datetime(string='Created At')
    updated_at = fields.Datetime(string='Updated At')
    state = fields.Selection(selection=[
        ('NEW', 'New'),
        ('PROCESSING', 'Processing'),
        ('PRE_TRANSIT', 'Pre Transit'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('PENDING_RETAILER_CONFIRMATION', 'Pending Retailer Confirmation'),
        ('BACKORDERED', 'Backordered'),
        ('CANCELED', 'Canceled'),
    ], string='State', help="""
        New: The order has not yet been accepted by the brand.
        Processing: The brand has accepted the order, and is in the process of fulfilling it.
        Pre Transit: The order has at least one shipment, but no shipments are in transit.
        In Transit: At least one of the shipments is in transit.
        Delivered: At least one of the shipments has been delivered.
        Pending Retailer Confirmation: The brand did not have sufficient quantity to fulfill the order; the retailer needs to decide whether they want to wait till the items are back in stock, or cancel.
        Backordered: The brand did not have sufficient quantity to fulfill the order and will ship it when items are back in stock.
        Canceled: The order was canceled by the brand or the retailer.
    """)
    
    # address = fields.Many2one(comodel_name='faire.address')
    ship_after = fields.Datetime(string='Ship After')
    # payout_costs
    payment_initiated_at = fields.Datetime(string='Payment Initiated At')
    retailer_id = fields.Char(string='Retailer ID')
    source = fields.Char(string='Source')
    expected_ship_date = fields.Datetime(string='Expected Ship Date')
    # customer = fields.
    customer_name = fields.Char(string='Customer Name')
    processing_at = fields.Datetime(string='Processing At')
    is_free_shipping = fields.Boolean(string='Is Free Shipping?')
    free_shipping_reason = fields.Selection(selection=[
        ('INSIDER_FREE_SHIPPING', 'Insider Free Shipping'),
        ('FAIRE_DIRECT', 'Faire Direct'),
        ('BRAND_DISCOUNT', 'Brand Discount'),
        ('FIRST_ORDER', 'First Order'),
        ('PROMO_CODE', 'Promo Code'),
        ('FREE_SHIPPING_THRESHOLD', 'Free Shipping Threshold'),
        ('EXTERNAL_FREE_SHIPPING_REASON_UNKNOWN', 'External Free Shipping Reason Unknown'),
    ], string='Free Shipping Reason', help="""
        Insider Free Shipping: The order has Insider free shipping.
        Faire Direct: The free shipping is due to a Faire Direct relationship.
        Brand Discount: The free shipping is due to a brand discount.
        First Order: The free shipping is due to this order being eligible for the first order promo for the retailer.
        Promo Code: The free shipping is due to a Promo Code being used.
        Free Shipping Threshold: The free shipping is due to the order meeting the brand-set Free Shipping threshold.
        External Free Shipping Reason Unknown: Unknown.
    """)
    
    # faire_covered_shipping_cost = fields.Json(string='Faire Covered Shipping Cost')
    # item_ids = fields.Many2one(comodel_name='faire.order.line')
    # shipment_ids =
    # brand_discounts = 
    
    order_line_ids = fields.One2many(comodel_name='faire.order.line', inverse_name='order_id')
    


    # 'id': 'bo_fhqq7dzfum'
    # 'display_id': 'FHQQ7DZFUM'
    # 'created_at': '2023-08-30T18:56:07.000Z'
    # 'updated_at': '2023-11-13T19:24:21.000Z'
    # 'state': 'DELIVERED'
    # 'address': {'id': 'a_a9r3ur67ym', 'name': 'Felina frank c/o My Circus Is My Haven', 'address1': '19665 East Via del Rancho', 'address2': '', 'postal_code': '85142', 'city': 'Queen Creek', 'state': 'Arizona', 'state_code': 'AZ', 'phone_number': '6025494485', 'country': 'United States', 'country_code': 'USA', 'company_name': 'My Circus Is My Haven', 'address_type': 'RESIDENTIAL'}
    # 'ship_after': '2023-08-31T19:15:00.000Z'
    # 'payout_costs': {'payout_fee_cents': 248, 'payout_fee_bps': 240, 'payout_flat_fee': {'amount_minor': 30, 'currency': 'USD'}, 'commission_cents': 2365, 'commission_bps': 1500, 'commission_flat_fee': {'amount_minor': 1000, 'currency': 'USD'}, 'payout_fee': {'amount_minor': 248, 'currency': 'USD'}, 'commission': {'amount_minor': 2365, 'currency': 'USD'}, 'total_payout': {'amount_minor': 6968, 'currency': 'USD'}, 'payout_protection_fee': {'amount_minor': 0, 'currency': 'USD'}, 'damaged_and_missing_items': {'amount_minor': 0, 'currency': 'USD'}, 'net_tax': {'amount_minor': 0, 'currency': 'USD'}, 'shipping_subsidy': {'amount_minor': 0, 'currency': 'USD'}, 'subtotal_after_brand_discounts': {'amount_minor': 9100, 'currency': 'USD'}, 'total_brand_discounts': {'amount_minor': 0, 'currency': 'USD'}, 'taxes': []}
    # 'payment_initiated_at': '2023-10-04T19:45:26.000Z'
    # 'retailer_id': 'r_9cynr7e2st'
    # 'source': 'MARKETPLACE'
    # 'expected_ship_date': '2023-08-31T19:15:00.000Z'
    # 'customer': {'first_name': 'Felina', 'last_name': 'Frank'}
    # 'processing_at': '2023-08-30T19:16:04.000Z'
    # 'is_free_shipping': True
    # 'free_shipping_reason': 'INSIDER_FREE_SHIPPING'
    # 'faire_covered_shipping_cost': {'amount_minor': 481, 'currency': 'USD'}
    # 'items': [{'id': 'oi_f5h3dyu4t6', 'created_at': '2023-08-30T18:22:10.000Z', 'updated_at': '2023-09-29T08:33:05.000Z', 'order_id': 'bo_fhqq7dzfum', 'product_id': 'p_8w4k4wyaas', 'variant_id': 'po_rdk3tuqcqk', 'quantity': 7, 'price_cents': 650, 'product_name': 'Car Diffuser: Sexy Sandlewood', 'variant_name': 'default', 'includes_tester': False, 'price': {...}, 'state': 'DELIVERED', 'customizations': [...], 'discounts': [...]}, {'id': 'oi_qjgynxgat2', 'created_at': '2023-08-30T18:22:10.000Z', 'updated_at': '2023-09-29T08:33:05.000Z', 'order_id': 'bo_fhqq7dzfum', 'product_id': 'p_5wk2qdnye5', 'variant_id': 'po_9b6e8qr5uy', 'quantity': 7, 'price_cents': 650, 'product_name': 'Car Diffuser: Newport', 'variant_name': 'default', 'includes_tester': False, 'price': {...}, 'state': 'DELIVERED', 'customizations': [...], 'discounts': [...]}]
    # 'shipments': [{'id': 's_zxzgu4cf5f', 'created_at': '2023-08-30T22:09:43.000Z', 'updated_at': '2023-09-02T21:29:24.000Z', 'order_id': 'bo_fhqq7dzfum', 'maker_cost_cents': 481, 'carrier': 'usps', 'tracking_code': '92001901755477300289848139', 'maker_cost': {...}, 'shipping_type': 'SHIP_ON_YOUR_OWN'}]
    # 'brand_discounts': []
    
    # @api.model
    # def get_views(self, views, options=None):
    #     res = super().get_views(views, options)
    #     doc = etree.XML(res['views']['form']['arch'] )
    #     for node in doc.xpath("//*[self::field]"):
    #         node.set('readonly', '1')
    #     res['views']['form']['arch'] = etree.tostring(doc)
    #     return res
    
    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('form', 'list'):
            # Set readonly for all fields
            for node in arch.xpath("//*[self::field]"):
                node.set('readonly', '1')
            # Set no create for form
            for node in arch.xpath("//form"):
                node.set('create', '0')
            # Set no create for list
            for node in arch.xpath("//list"):
                node.set('create', '0')
        return arch, view
