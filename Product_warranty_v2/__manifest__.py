{
    'name': "Warranty V2",
    'version': '1.0',
    'depends': ['base', 'account', 'product'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/warranty2_security.xml',
        'security/ir.model.access.csv',
        'security/warranty_rules.xml',
        'data/ir_sequence_warranty.xml',
        # 'data/warranty_location.xml',
        'views/product_warranty_views.xml',
        'views/template_views.xml',
    ],
}
