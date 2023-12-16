from odoo import fields, models
from odoo.exceptions import UserError


class AutomatedPurchase(models.Model):
    """to inherit the product view page and add a button to create rfq"""
    _inherit = "product.template"

    def action_create_rfq(self):
        """when create rfq button is pressed a wizard should pop up to show the quantity and price of the product """
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.wizard',
            'view_id': self.env.ref('automated_purchase.purchase_wizard_form').id,
            'target': 'new',
            'context': {
                'default_product_id': self.id,
            }
        }


class PurchaseWizard(models.TransientModel):
    """creating a wizard when create rfq button is pressed"""
    _name = "purchase.wizard"

    product_id = fields.Many2one('product.template')
    product_name = fields.Char(related='product_id.name')
    quantity = fields.Integer(string="Quantity", default="1")
    price = fields.Float(string="price")

    def confirm_rfq(self):
        """when confirm button is pressed an rfq is created for the product"""
        product_product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.product_id.id)]).id
        if not self.product_id.seller_ids:
            raise UserError('choose a vendor')
        else:
            seller_id = self.product_id.seller_ids[0]
            vendor_id = seller_id.partner_id.id
            vendor_price = seller_id.price
            seller_check = self.env['purchase.order'].search([('partner_id', '=', vendor_id), ('state', '=', 'draft')])
            if seller_check:
                seller_check[0].order_line = fields.Command.create({
                    'product_id': self.product_id.id,
                    'product_qty': self.quantity,
                    'price_unit': self.price,
                })
                seller_check[0].button_confirm()
            else:

                purchase_id = self.env['purchase.order'].create({'partner_id': vendor_id,
                                                                 'order_line': [
                                                                     fields.Command.create(
                                                                         {
                                                                             'product_id': product_product_id,
                                                                             'product_qty': self.quantity,
                                                                             'price_unit': vendor_price}),
                                                                 ]
                                                                 })
                purchase_id.button_confirm()

