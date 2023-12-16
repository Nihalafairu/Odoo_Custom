{
    'name': "Warranty",
    'version': '16.0.1.0.0',
    'category': 'Warranty',
    'summary': 'Product Warranty',
    'depends': ['base', 'sale', 'product', 'account', 'stock', 'mail', 'website'],
    'author': "Nihala",
    'description': "We can issue warranty to products",

    'data': [
        'security/warranty_security.xml',
        'security/ir.model.access.csv',
        'security/warranty_ir_rule.xml',
        'data/ir_sequence_warranty.xml',
        'data/stock_location.xml',
        'data/website_view.xml',
        'views/product_warranty_views.xml',
        'wizard/warranty_wizard_view.xml',
        'views/product_warranty_product_view.xml',
        'views/product_warranty_invoice_view.xml',
        'views/warranty_website_view.xml',
        'views/warranty_snippet_view.xml',
        'views/warranty_snippet_template.xml',
        'report/warranty_report_view.xml',
        'report/ir_action_report.xml',

    ],
    "assets":
        {"web.assets_backend":
            [
                'product_warranty/static/src/js/action_manager.js',
            ],
            "web.assets_frontend":
                [
                    'product_warranty/static/src/js/warranty_website.js',
                    'product_warranty/static/src/js/warranty_snippet.js',
                    'product_warranty/static/src/xml/warranty_website_snippet.xml',

                ],
        },

    'installable': True,
    'application': True,
}
