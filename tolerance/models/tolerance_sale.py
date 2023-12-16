from odoo import fields, models


class ToleranceSale(models.Model):
    """to add tolerance field in the sale order lines"""
    _inherit = "sale.order.line"

    tolerance = fields.Integer(string="Tolerance", related="order_partner_id.tolerance", readonly=False, store=True)
