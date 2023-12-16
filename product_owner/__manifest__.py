{
    'name': "Product Owner",
    'version': '16.0.1.1.1',
    'category': 'bom_cart',
    'depends': ['base','point_of_sale','sale','product'],
    'author': "Nihala",
    'description': "Show Product owner in line and reciept",
    'data': [
        'views/product_template_owner_view.xml',
        'views/change_name_view.xml',
    ],
    "assets":
            {"point_of_sale.assets":
                [
                    'product_owner/static/src/js/product_owner.js',
                    'product_owner/static/src/xml/pos_reciept_line.xml',
                    'product_owner/static/src/xml/pos_order_line.xml'
                ]
            },
    'installable': True,
}
