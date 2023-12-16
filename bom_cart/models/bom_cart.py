from ast import literal_eval

from odoo import fields, models, api


class Confsetting(models.TransientModel):
    _inherit = "res.config.settings"

    product_cart = fields.Boolean(config_parameter='bom_cart.product_cart', string="Bom Products")
    product_ids = fields.Many2many('product.product', relation="bom_product_ids_rel", string="products")

    def set_values(self):
        res = super(Confsetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('bom_cart.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(Confsetting, self).get_values()
        product_list = self.env['ir.config_parameter'].sudo().get_param('bom_cart.product_ids')
        res.update(product_ids=[(6, 0, literal_eval(product_list))] if product_list else False,)
        return res
