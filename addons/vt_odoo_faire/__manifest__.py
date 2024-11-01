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
    ],
    'demo': [
    ],
    'data': [
        'data/data_faire_permission_scope.xml',
        'security/ir.model.access.csv',
        'views/faire_oauth_views.xml',
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