# -*- coding: utf-8 -*-
{
    'name': "Cybro Theme",
    'version': '16.0.1.1.1',
    'summary': "cybro theme",
    'category': 'Theme',
    'depends': ['website'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'sequence': 110,
    'description': "add icon in systray and show weather notification",
    'data': [
        'data/pages/about_us.xml',
        'data/menu.xml'

    ],
    'images':[
        'static/description/clean_description.jpg',
        'static/description/clean_screenshot.jpg'
    ],
    "assets":
        {"web._assets_primary_variables":
                [
                   '/theme_cybro/static/scss/cybro_theme.scss'
                ]

        },


    'license': 'LGPL-3'
}
