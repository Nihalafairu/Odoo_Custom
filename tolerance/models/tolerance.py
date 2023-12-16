from odoo import fields, models


class Tolerance(models.Model):
    """to add a tolerance field in the customer form"""
    _inherit = "res.partner"

    tolerance = fields.Integer(string="Tolerance")





