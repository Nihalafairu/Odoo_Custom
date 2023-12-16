# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PosCombo(models.Model):
    """used to create details of combo products inside a product"""
    _name = "pos.combo"

    category_id = fields.Many2one('pos.category', string="Category")
    product_ids = fields.Many2many('product.template', string="Products", domain="[('pos_categ_id','=',category_id)]")
    required = fields.Boolean(string='Is Required')
    count = fields.Integer(string="Item Count")
    template_id = fields.Many2one('product.template')

    @api.model
    def get_combo_details(self, arg):
        """this function is used to pass combo product details to rpc call """
        combo_product_id = self.env['pos.combo'].browse(arg)
        combo_details_required = []
        combo_details_optional = []
        for combo in combo_product_id:
            category = combo.category_id.display_name
            products = {}
            prod_id = {}
            for prod in combo.product_ids:
                products[prod.name] = prod.image_1920
                prod_id[prod.id] = prod.name
            required = combo.required
            count = combo.count
            if required:
                required = {
                    'category_id': category,
                    'product': products,
                    'count': count,
                }
                combo_details_required.append(required)
            else:
                optional = {
                    'category_id': category,
                    'product': products,
                    'count': count,
                    'id': prod_id
                }
                combo_details_optional.append(optional)

        data = {
            'required': combo_details_required,
            'optional': combo_details_optional
        }
        return data
