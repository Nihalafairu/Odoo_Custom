from odoo import fields, models


class SalePayment(models.Model):
    _inherit = "sale.order"

    payment_id = fields.Many2one('account.payment')

    def action_create_payment(self):
        self._create_invoices()
        self.invoice_ids.action_post()
        payment = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'amount': self.amount_total,
            'date': self.date_order,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'ref': self.invoice_ids.name,
            'move_type': 'out_invoice'

        })
        self.payment_id = payment
        self.payment_id.action_post()
        self.invoice_ids.payment_state = 'paid'

