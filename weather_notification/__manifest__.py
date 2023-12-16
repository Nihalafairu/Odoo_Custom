# -*- coding: utf-8 -*-
{
    'name': "Weather Notificatoin",
    'version': '16.0.1.1.1',
    'summary': "Weather Notification",
    'category': 'weather_notifications',
    'depends': ['base', 'web'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "add icon in systray and show weather notification",
    'data': [
        'views/weather_conf.xml',
    ],
    "assets":
        {"web.assets_backend":
                [
                    'weather_notification/static/src/js/weather_notification.js',
                    'weather_notification/static/src/xml/weather_icon.xml',
                ]

        },


    'installable': True,
    'license': 'LGPL-3'
}
