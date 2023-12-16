# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class InventoryDashboard(models.Model):
    """to create dashboard"""
    _name = "inventory.dashboard"

    @api.model
    def incoming_stock(self, arg):
        """to give the incoming stock details to dashboard"""

        if int(arg) == 0:
            stock_incoming = self.env['stock.move'].search([('location_id.usage', 'not in', ('internal', 'transit')),
                                                            ('location_dest_id.usage', 'in', ('internal', 'transit'))])
        else:
            date_untill = fields.datetime.today().date() - \
                          timedelta(days=int(arg))

            stock_incoming = self.env['stock.move'].search([('location_id.usage', 'not in', ('internal', 'transit')),
                                                            ('location_dest_id.usage', 'in', ('internal', 'transit')),
                                                            ('create_date', '>', date_untill)])
        incoming_products = []
        incoming_products = stock_incoming.product_id
        stock_details = []

        for product in incoming_products:
            record = {
                product.product_tmpl_id.name: product.qty_available
            }
            stock_details.append(record)

        return stock_details

    @api.model
    def outgoing_stock(self, arg):
        """to give outgoing stock details to dashboard"""
        if int(arg) == 0:

            stock_outgoing = self.env['stock.move'].search([('location_id.usage', 'in', ('internal', 'transit')),
                                                            ('location_dest_id.usage', 'not in',
                                                             ('internal', 'transit'))])
        else:
            date_untill = fields.datetime.today().date() - \
                          timedelta(days=int(arg))
            stock_outgoing = self.env['stock.move'].search([('location_id.usage', 'in', ('internal', 'transit')),
                                                            ('location_dest_id.usage', 'not in',
                                                             ('internal', 'transit')),
                                                            ('create_date', '>', date_untill)])

        outgoing_products = []
        outgoing_products = stock_outgoing.product_id
        stock_details = []
        for product in outgoing_products:
            record = {
                product.product_tmpl_id.name: product.qty_available
            }
            stock_details.append(record)

        return stock_details

    @api.model
    def location_stock(self):
        """to give location wise stock details to dashboard """
        stock_locations = self.env['stock.location'].sudo().search([])
        location_details = []
        for location in stock_locations:
            prod = []
            if location.quant_ids.product_id:
                for products in location.quant_ids.product_id:
                    prod.append(products.product_tmpl_id.name)
                record = {
                    location.name: prod
                }
                location_details.append(record)

        return location_details

    @api.model
    def product_expense(self):
        """to give expense of a product"""
        products = self.env['product.template'].sudo().search([])
        expense_details = []
        for product in products:
            name = product.name
            cost = product.standard_price
            record = {
                name: cost
            }
            expense_details.append(record)

        return expense_details

    @api.model
    def stock_valuation(self):
        """stock valuation details of a product"""
        products = products = self.env['product.product'].sudo().search([])
        stock_valuation = []
        for product in products:
            name = product.product_tmpl_id.name
            quantity = product.qty_available
            record = {
                name: quantity
            }
            stock_valuation.append(record)

        return stock_valuation

    @api.model
    def internal_transfers(self):
        """transfers of a product"""
        mngr_group = self.env.ref('stock.group_stock_manager')
        picking_type = self.env['stock.picking.type'].search([('sequence_code', '=', 'INT')])
        transfer_details = []
        if self.env.user in mngr_group.users:
            transfers = self.env['stock.picking'].search([('picking_type_id', '=', picking_type.id)])
            for transfer in transfers:
                pro_name = transfer.move_ids.product_id.product_tmpl_id.name
                pro_quant = transfer.move_ids.quantity_done
                record = {
                    pro_name: pro_quant
                }
                transfer_details.append(record)

        else:
            transfers = self.env['stock.picking'].search([('picking_type_id', '=', picking_type.id),
                                                          ('create_uid','=',self.env.user.id)])
            transfer_details = []
            for transfer in transfers:
                pro_name = transfer.move_ids.product_id.product_tmpl_id.name
                pro_quant = transfer.move_ids.quantity_done
                record = {
                    pro_name: pro_quant
                }
                transfer_details.append(record)

        return transfer_details
