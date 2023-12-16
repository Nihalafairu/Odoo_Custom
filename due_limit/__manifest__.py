{
    'name': "Due Limit",
    'version': '16.0.1.1.1',
    'category': 'bom_cart',
    'depends': ['base','point_of_sale','sale'],
    'author': "Nihala",
    'description': "Add Due Limit to Customer",
    'data': [
        'views/customer_template_view.xml',
    ],
    "assets":
            {"point_of_sale.assets":
                [
                    'due_limit/static/src/js/pos_limit.js'
                ]
            },
    'installable': True
}
