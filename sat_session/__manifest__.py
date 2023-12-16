# -*- coding: utf-8 -*-
{
    'name': "Sat Session",
    'version': '16.0.1.1.1',
    'summary': "Sat Session",
    'depends': ['base'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "creating name and age field without python",
    'data': [
        'security/ir.model.access.csv',
        'views/sat_field_view.xml',


    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
