from odoo import fields, models


class ProductOwner(models.Model):
    _inherit = 'product.product'

    owner_id = fields.Many2one('res.partner', string="Product Owner")
