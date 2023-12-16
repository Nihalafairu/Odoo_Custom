from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SoApproval(models.Model):
    """to inherit sale order and to add new fields """
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[
        ('waiting', 'Waiting for Approval'),
        ('sent', 'Quotation Sent')
    ])

    def action_send_manager(self):
        """to change the state of button to waiting for approval"""
        self.state = 'waiting'

    def action_send_approve(self):
        """to change the state to Sale Order"""
        self.state = 'sale'

    def action_send_disapprove(self):
        """to change the state and update the sales price inside the product"""
        for record in self.order_line:
            record.price_unit = record.product_id.list_price
        self.state = 'draft'

    def validation_error(self):
        """to show validation error when salesperson changes the price from order lines"""
        for record in self:
            if self.user_has_groups('so_approval.group_sale_salesperson,'
                                    '!so_approval.group_sale_manager'):
                for i in record.order_line:
                    if (i.price_unit > i.product_id.list_price or
                            i.price_unit < i.product_id.list_price):
                        raise ValidationError(
                            _('Unit Price have changed, get approval from the manager'))

    def action_confirm(self):
        """show validation error when salesperson changes the price and confirms the order """
        self.validation_error()
        super().action_confirm()

    def action_quotation_send(self):
        """show validation error when salesperson changes the price and confirms the order"""
        self.validation_error()
        super().action_quotation_send()
