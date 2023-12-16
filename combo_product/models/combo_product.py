# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ComboProducts(models.Model):
    """ to add page and fields to product template"""
    _inherit = "product.template"

    combo_ids = fields.One2many('pos.combo', "template_id")
    combo = fields.Boolean(string="Is Combo")
    combo_test = fields.Boolean(compute='_compute_combo', store=True)


