{
    'license': 'LGPL-3',
    'name': "Odoo-Square",
    'summary': "Odoo-Square Integration",
    'author': "Victor Imannuel (Child of God)",
    'website': "",
    'support': 'victorimannuel.dev@gmail.com',
    'category': 'Extra Tools',
    'version': '18.0',
    'depends': [
        'web',
        'sale',
    ],
    'demo': [
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/square_card_view.xml',
        'views/sale_order_views.xml',
        # 'views/my_component_view.xml',
    ],
    'images': [
    ],
    'assets': {
        # 'web.assets_frontend': [
            # 'vt_odoo_square/static/src/js/app.js',
            # 'vt_odoo_square/static/src/js/my_component.js',
            # 'vt_odoo_square/static/src/js/initialize_component.js',
        # ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}