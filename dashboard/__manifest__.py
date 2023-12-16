# -*- coding: utf-8 -*-
{
    'name': "Inventory Dashboard",
    'version': '16.0.1.1.1',
    'summary': "Inventory Dashboard",
    'category': 'inventory_dashboard',
    'depends': ['base', 'stock','sale','product'],
    'author': "Nihala",
    'website':"www.odoo.com",
    'description': "Add dashboard to stock module",
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_menu_view.xml',

    ],
    "assets":
        {"web.assets_backend":
                [
                    'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.js.map',
                    'dashboard/static/src/xml/dashboard_template.xml',
                    'dashboard/static/src/assets/vendors/mdi/css/materialdesignicons.min.css',
                    'dashboard/static/src/assets/vendors/css/vendor.bundle.base.css',
                    'dashboard/static/src/assets/images/favicon.ico',
                    'dashboard/static/src/js/inventory_dashboard.js',
                ]

        },


    'installable': True,
    'license': 'LGPL-3'
}
