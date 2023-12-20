# -*- coding: utf-8 -*
from ast import literal_eval

from odoo import models, fields, api


class ConfSetting(models.TransientModel):
    """Add new fields in inventory settings"""
    _inherit = "res.config.settings"

    stock_warning = fields.Boolean(config_parameter='stock_warning.stock_warning', string="Stock Warning Email")
    threshold_quantity = fields.Integer(config_parameter='stock_warning.threshold_quantity',
                                        string="Threshold Quantity")
    product_ids = fields.Many2many('product.product', relation="stock_product_ids_rel", string="Products")

    def set_values(self):
        res = super(ConfSetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('stock_warning.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ConfSetting, self).get_values()
        product_list = self.env['ir.config_parameter'].sudo().get_param('stock_warning.product_ids')
        res.update(product_ids=[(6, 0, literal_eval(product_list))] if product_list else False, )
        return res


