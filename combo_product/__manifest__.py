# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Combo Product',
    'version': '16.0.1.1.1',
    'category': 'Sales/Sales',
    'summary': 'Combo Products',
    'description': """
           combo products in point of sale
    """,
    'depends': ['point_of_sale', 'sale'],
    'data': [
            'security/ir.model.access.csv',
            'views/pos_combo_view.xml',
    ],
    'assets':{
        "point_of_sale.assets":[
            'combo_product/static/src/scss/ribbon_style.scss',
            'combo_product/static/src/xml/product_image_pos.xml',
            'combo_product/static/src/xml/combo_popup.xml',
            'combo_product/static/src/xml/combo_order.xml',
            'combo_product/static/src/xml/combo_recipt.xml',
            'combo_product/static/src/js/combo_popup.js',
            'combo_product/static/src/js/combo_product.js',
            'combo_product/static/src/js/combo_receipt.js',

        ]
    },

    'installable': True,
    'auto_install': False,
        'license': 'LGPL-3',
}
