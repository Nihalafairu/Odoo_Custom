{
    'name': "Automated Purchase",
    'version': '16.0.1.1.1',
    'category': 'purchase_order',
    'depends': ['base', 'product','purchase'],
    'author': "Nihala",
    'description': "Automated purchase order should be done when create rfq button is pressed in the product page",
    'data': [
        'security/ir.model.access.csv',
        'views/automated_purchase.xml',
        'views/purchase_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}
