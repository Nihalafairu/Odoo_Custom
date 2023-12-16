from odoo import fields, models, api
from ast import literal_eval


class Confsetting(models.TransientModel):
    _inherit = "res.config.settings"

    valuation = fields.Boolean(config_parameter='inventory_valuation.valuation', string="Valuation")
    user_ids = fields.Many2many('res.users', relation="stock_user_ids_rel", string="Specified Users")

    def set_values(self):
        res = super(Confsetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('inventory_valuation.user_ids', self.user_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(Confsetting, self).get_values()
        user_list = self.env['ir.config_parameter'].sudo().get_param('inventory_valuation.user_ids')
        res.update(user_ids=[(6, 0, literal_eval(user_list))] if user_list else False, )
        return res
