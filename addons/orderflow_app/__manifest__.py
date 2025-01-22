{
    'license': 'LGPL-3',
    'name': "OrderFlow App",
    'summary': "",
    'author': "Victor Imannuel (Child of God)",
    'website': "",
    'support': 'victorimannuel.dev@gmail.com',
    'category': 'Sale',
    'version': '18.0',
    'depends': [
        # Default odoo module
        'sale_management',
        'sale',
        'stock',
        'account',
        'utm',
        'mail',
        'contacts',
        'mass_mailing',
        'mass_mailing_sms',
        'im_livechat',
        'spreadsheet_dashboard',
        'website_sale',
        
        # Custom module
        'vt_odoo_faire',
        'ica_web_responsive',
        'muk_web_theme',
        'web_window_title',
        'web_chatter_position_cr',
        'ecommerce_website_minimum_order_quantity',
        
    ],
    'demo': [
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/product_pricelist_views.xml',
        'views/delivery_form_templates.xml',
        
        'data/ir_actions.xml',
        'views/menu_views.xml',
    ],
    'images': [
    ],
    'assets': {
        'web.assets_backend': [
            'orderflow_app/static/src/product_configurator_dialog.js',
        ],
        'web.assets_frontend': [
            'orderflow_app/static/src/checkout.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}