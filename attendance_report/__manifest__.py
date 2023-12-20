# -*- coding: utf-8 -*-
{
    'name': "Daily Attendance Report",
    'version': '16.0.1.1.1',
    'summary': "Daily Attendance Report",
    'category': 'attendance_report',
    'depends': ['base', 'hr'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "create daily attendance report",
    'data': [
        'security/ir.model.access.csv',
        'data/ir.cron.xml',
        'views/daily_attendance_view.xml',
    ],

    'installable': True,
    'license': 'LGPL-3'
}
