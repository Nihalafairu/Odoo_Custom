from odoo import fields, models, api, _
from datetime import timedelta, datetime


class ProductWarrantyV2(models.Model):
    _name = "product.warranty2"

    _rec_name = 'reference_no'
    reference_no = fields.Char(string='Order Reference',
                               readonly=True, default=lambda self: _(''))
    invoice_id = fields.Many2one('account.move', string="Invoice Id", domain="[('move_type','=','out_invoice')]")
    product_id = fields.Many2one('product.product', string="", domain="[('id','in',product_ids)]")
    product_ids = fields.Many2many('product.product', compute="compute_onchange_invoice")
    lot_serial = fields.Many2one('stock.lot', domain="[('product_id','=',product_id)]", )
    request_date = fields.Date(default=datetime.today())
    customer_id = fields.Many2one('res.partner', related='invoice_id.partner_id')
    purchase_date = fields.Date(related='invoice_id.invoice_date')
    warranty_expiry_date = fields.Date(compute="_compute_expiry_date", store=True)
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('cancel', 'cancel')])

    @api.depends('invoice_id')
    def compute_onchange_invoice(self):
        self.product_ids = self.invoice_id.invoice_line_ids.mapped('product_id').ids

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'product.warranty2')
        res = super(ProductWarrantyV2, self).create(vals)
        print(res)
        return res

    @api.depends('product_id', 'purchase_date', 'product_id.warranty_period')
    def _compute_expiry_date(self):
        for record in self:
            if record.product_id:
                record.warranty_expiry_date = record.purchase_date + timedelta(days=record.product_id.warranty_period)

    def action_submit(self):
        self.state = 'to_approve'

    def action_approve(self):
        self.state = 'approved'
