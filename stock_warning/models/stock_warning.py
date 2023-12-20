# -*- coding: utf-8 -*-
from odoo import models


class StockWarning(models.Model):
    """To send stock warning msg to stock manager"""
    _inherit = "product.product"

    def stock_warning(self):
        """send mail when on hand quantity of a product is less than threshold quantity"""

        product_ids = self.env['ir.config_parameter'].sudo().get_param('stock_warning.product_ids')
        threshold_quantity = self.env['ir.config_parameter'].sudo().get_param('stock_warning.threshold_quantity')
        stock_warning = self.env['ir.config_parameter'].sudo().get_param('stock_warning.stock_warning')

        if stock_warning:
            product_id = product_ids[1:-1]
            if product_id:
                product_check = product_id.split(", ")
                products = [int(prod) for prod in product_check]
                context = {}
                for pro_id in products:
                    product_mail = self.env['product.product'].browse(pro_id)
                    if int(threshold_quantity) > product_mail.qty_available:
                        stock_manager_mail = self.env.ref('stock.group_stock_manager').users.mapped('login')
                        email_values = {
                            'email_to': stock_manager_mail[0],
                            'email_cc': ', '.join(stock_manager_mail[1:]),
                            'subject': "stock updation Warning(" + product_mail.product_tmpl_id.name + ")!!!",
                        }

                        context.update({
                            'product_id': product_mail.product_tmpl_id.name,
                            'product_qty': product_mail.qty_available
                        })

                        mail_template = self.env.ref('stock_warning.stock_warning_mail')
                        mail_template.with_context(**context).send_mail(product_mail.id, force_send=True, email_values=email_values)

