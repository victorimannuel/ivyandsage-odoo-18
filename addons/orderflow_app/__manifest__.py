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
        'sale_management',
        'stock',
        'account',
        'mass_mailing',
        'im_livechat',
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
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}