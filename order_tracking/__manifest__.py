{
    'name': "Order Tracking",
    'version': '16.0.1.1.1',
    'category': 'order_tracking',
    'depends': ['base','website','website_sale','stock','product'],
    'author': "Nihala",
    'description': "Track your Orders",
    'data': [
        'security/ir.model.access.csv',
        'data/website_tracking.xml',
        'views/order_tracking_view.xml',
        'views/website_tracking_view.xml',


    ],
    "assets":
            {"web.assets_frontend":
                [
                    'order_tracking/static/src/scss/order_tracking_view.scss',
                ]
            },
    'installable': True,
}
