{
    'name': "Tolerance",
    'version': '16.0.1.1.1',
    'category': 'tolerance',
    'depends': ['base', 'sale','contacts'],
    'author': "nihala",
    'description': "adding tolerance",
    'data': [
        'security/ir.model.access.csv',
        'views/tolerance_customer_view.xml',
        'views/tolerance_order_line_view.xml',
        'views/tolerance_stock_picking_view.xml',
        'wizard/tolerance_wizard_view.xml',

    ],
    'installable': True
}
