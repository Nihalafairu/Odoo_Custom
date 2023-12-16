# -*- coding: utf-8 -*-
{
    'name': "Contact Creation",
    'version': '16.0.1.1.1',
    'summary': "Contact creation from survey",
    'category': 'contact_creation',
    'depends': ['base', 'survey', 'contacts'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "Contact creation from survey",
    'data': [
        'security/ir.model.access.csv',
        'views/contact_relation_view.xml',
    ],


    'installable': True,
    'license': 'LGPL-3'
}
