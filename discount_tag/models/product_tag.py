from odoo import models, fields


class DueLimit(models.Model):
    """to inherit the product and add new field discount price"""
    _inherit = "product.product"

    discount = fields.Float(string="Discount Tag")

