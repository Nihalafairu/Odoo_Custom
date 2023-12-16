# -*- coding: utf-8 -*-
{
    'name': "Employee Helpdesk",
    'version': '16.0.1.1.1',
    'summary': "Employee Helpdesk",
    'category': 'employee_helpdesk',
    'depends': ['base', 'website','hr'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "Employee can raise help desk ticket through website",
    'data': [
        'security/helpdesk_security.xml',
        'security/help_ir_rule.xml',
        'security/ir.model.access.csv',
        'data/website_help_view.xml',
        'data/ir_sequence_helpdesk.xml',
        'views/employee_help_view.xml',
        'views/website_help_form_view.xml'

    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
