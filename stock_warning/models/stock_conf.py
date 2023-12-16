# -*- coding: utf-8 -*
from ast import literal_eval

from odoo import models, fields


class Confsetting(models.TransientModel):
    _inherit = "res.config.settings"

    stock_warning = fields.Boolean(config_parameter='stock_warning.stock_warning', string="Stock Warning Email")
    threshold_quantity = fields.Integer(config_parameter='stock_warning.threshold_quantity',
                                        string="Threshold Quantity")
    product_id = fields.Many2one('product.product', config_parameter='stock_warning.product_id', string="product")
