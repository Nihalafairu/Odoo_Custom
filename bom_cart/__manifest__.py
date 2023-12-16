{
    'name': "BOM Cart",
    'version': '16.0.1.1.1',
    'category': 'bom_cart',
    'depends': ['base','website','website_sale','mrp','sale'],
    'author': "Nihala",
    'description': "Add BOM to cart",
    'data': [
        'views/website_config_view.xml',
        'views/website_cart_view.xml',
    ],
    'installable': True,
}
