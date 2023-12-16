from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    has_warranty = fields.Boolean(string='Has Warranty', default=False)
    warranty_period = fields.Integer(string='Warranty Period (Days)')
    warranty_type = fields.Selection(string='Warranty Type',
                                     selection=[('Service Warranty', 'Service Warranty'),
                                                ('Replacement Warranty', 'Replacement Warranty')]
                                     )
