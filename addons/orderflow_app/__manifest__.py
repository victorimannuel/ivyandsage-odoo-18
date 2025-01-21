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
        'stock',
        'account',
        'utm',
        'mail',
        'contacts',
        'sale',
        'mass_mailing',
        'mass_mailing_sms',
        'im_livechat',
        'spreadsheet_dashboard',
        'website_sale',
        
        # Custom module
        'vt_odoo_faire',
        'muk_web_theme',
        'web_chatter_position_cr',
        'web_window_title',
        
    ],
    'demo': [
    ],
    'data': [
        'views/sale_order_views.xml',
        'data/ir_actions.xml',
        'views/menu_views.xml',
    ],
    'images': [
    ],
    'assets': {
        'web.assets_backend': [
            'orderflow_app/static/src/product_configurator_dialog.js',
            # 'orderflow_app/static/src/product.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}