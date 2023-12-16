from odoo import fields, models, api, _


class ProductTemplateV2(models.Model):
    _inherit = 'product.template'

    has_warranty = fields.Boolean()
    warranty_period = fields.Integer()
    warranty_type = fields.Selection(
        selection=[('service', 'Service Warranty'), ('replacement', 'Replacement Warranty')])
