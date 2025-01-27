{
    'license': 'LGPL-3',
    'name': "Faire v2",
    'summary': "Odoo-Faire Integration",
    'author': "Victor Imannuel (Child of God)",
    'website': "",
    'support': 'victorimannuel.dev@gmail.com',
    'category': 'Extra Tools',
    'version': '18.0',
    'depends': [
        'account',
        'base',
        'sale',
        'product',
    ],
    'demo': [
    ],
    'data': [
        'data/data_faire_permission_scope.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        
        'views/res_config_settings_views.xml',
        'views/faire_oauth_views.xml',
        'views/faire_api_service_views.xml',
        'views/faire_order_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        
        'views/menu_views.xml',
        'views/success_page_template.xml',
    ],
    'images': [
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}