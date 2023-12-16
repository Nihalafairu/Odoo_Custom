# -*- coding: utf-8 -*-
{
    'name': "Stock Warning",
    'version': '16.0.1.1.1',
    'summary': "Stock Warning Email",
    'category': 'stock_warning',
    'depends': ['base', 'stock','mail'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "Send a stock warning email to the inventory manager.",
    'data': [
        'views/stock_warning_config.xml',

    ],

    'installable': True,
    'license': 'LGPL-3'
}
