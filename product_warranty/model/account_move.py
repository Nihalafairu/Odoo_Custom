from odoo import api, fields, models


class WarrantyInvoice(models.Model):
    # _name = 'warranty.invoice'
    _inherit = 'account.move'

    warranty_request = fields.One2many('product.warranty', 'invoice_id')

    reference_no = fields.Char(related='warranty_request.reference_no')






