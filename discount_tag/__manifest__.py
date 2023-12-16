{
    'name': "Discount Tag",
    'version': '16.0.1.1.1',
    'category': 'discount_tag',
    'depends': ['base', 'point_of_sale', 'sale'],
    'author': "Nihala",
    'description': "Add discount tag to products",
    'data': [
        'views/product_tag_view.xml',

    ],
    "assets":
        {"point_of_sale.assets":
            [
                'discount_tag/static/src/xml/pos_reciept_tag.xml',
                'discount_tag/static/src/xml/pos_product_tag.xml',
                'discount_tag/static/src/js/pos_discount_tag.js'
            ]
        },

    'installable': True
}
