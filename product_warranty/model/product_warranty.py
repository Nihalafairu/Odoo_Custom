from odoo import api, fields, models, _
from datetime import datetime, timedelta


class ProductWarranty(models.Model):
    """This model is used for storing the warranty request details"""
    _name = "product.warranty"
    _description = "Product Warranty"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'reference_no'

    reference_no = fields.Char(string='Order Reference',
                               readonly=True, default=lambda self: _(''))

    invoice_id = fields.Many2one('account.move', string='Invoice', index=True,  required=True, domain="[('move_type', '=', "
                                                                                         "'out_invoice'),('state','!=','draft')]",
                                 selection=[('posted', 'Posted')],
                                 )

    product_id = fields.Many2one('product.product', required=True,
                                 domain="[('id','in',product_ids),('has_warranty','=',True)]")
    request_date = fields.Date(default=datetime.today())
    customer_details_id = fields.Many2one('res.partner', related='invoice_id.partner_id')
    purchase_date = fields.Date(related='invoice_id.date')

    lot_serial_id = fields.Many2one('stock.lot', domain="[('product_id','=',product_id)]",
                                    )
    product_ids = fields.Many2many('product.product', compute='_compute_invoice_ids')

    warranty_expire_date = fields.Date(compute="compute_expire_date", store=True)
    smart_check = fields.Boolean(string="check", default=False)
    website_check = fields.Boolean(default=False)
    product_image = fields.Image( related='product_id.image_1920')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('product_received', 'Product Received'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, default='draft')

    @api.depends('invoice_id')
    def _compute_invoice_ids(self):
        """This function is used to get the products in the invoice"""
        self.product_ids = self.invoice_id.invoice_line_ids.mapped('product_id').ids

    @api.model
    def create(self, vals):
        """This function is used to create the sequence number"""
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'product.warranty')
            # print(vals, "kk")
        res = super().create(vals)

        return res

    @api.depends('purchase_date', 'product_id.warranty_period', 'product_id')
    def compute_expire_date(self):
        # print(self)
        """This function is used to calculate the expiration date of the product"""
        for record in self:
            if record.product_id:
                record.warranty_expire_date = record.purchase_date + timedelta(
                    days=record.product_id.warranty_period)

    def action_submit(self):
        """state changes to to_approve  when submit button is presses"""
        self.state = 'to_approve'

    def action_approve(self):
        """state changes to approved when approve button is pressed & created a moves history"""
        self.state = 'approved'

        location_warranty = self.env.ref('product_warranty.location_warranty')
        customer_location = self.env.ref('stock.stock_location_customers')
        move = self.env['stock.move'].create({
            'name': self.reference_no,
            'location_id': customer_location.id,
            'location_dest_id': location_warranty.id,
            'product_id': self.product_id.id,
            'move_line_ids': [fields.Command.create({
                'product_id': self.product_id.id,
                'lot_id': self.lot_serial_id.id,
                'qty_done': 1,

            })],
            'origin': self.reference_no

        })
        self.smart_check = True

        move._action_confirm()
        move._action_assign()
        move._action_done()
        self.state = 'product_received'

    def action_cancel(self):
        """state is changed"""
        self.state = 'cancel'

    def action_return(self):
        """state is changed and created move"""
        location_warranty = self.env.ref('product_warranty.location_warranty')
        customer_location = self.env.ref('stock.stock_location_customers')
        move = self.env['stock.move'].create({
            'name': self.reference_no,
            'location_id': location_warranty.id,
            'location_dest_id': customer_location.id,
            'product_id': self.product_id.id,
            'move_line_ids': [fields.Command.create({
                'product_id': self.product_id.id,
                'lot_id': self.lot_serial_id.id,
                'qty_done': 1
            })],
            'origin': self.reference_no
        })
        self.smart_check = True

        move._action_confirm()
        move._action_assign()
        move._action_done()

        self.state = 'done'

    def action_smart(self):
        """created a smart button"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Moves',
            'view_mode': 'tree',
            'res_model': 'stock.move.line',
            'domain': [('origin', '=', self.reference_no)],
            'context': "{'create': False}"
        }
