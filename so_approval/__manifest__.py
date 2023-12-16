{
    'name': "SO Approval",
    'version': '16.0.1.1.1',
    'category': 'so_approval',
    'depends': ['base', 'sale', ],
    'author': "Nihala",
    'description': "Sale Order Approval",
    'data': [
        'security/so_groups.xml',
        'security/ir.model.access.csv',
        'views/so_view.xml',
    ],
    'installable': True,
    'application': True,
}
