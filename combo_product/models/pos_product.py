# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class PosSession(models.Model):
    """this used to load some fields to pos session"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """this used to load some fields to pos session"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['combo_ids', 'combo', 'combo_test'])
        return result
