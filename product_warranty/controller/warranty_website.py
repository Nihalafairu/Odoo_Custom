from odoo.http import Controller, request, route
from datetime import timedelta, datetime


class WarrantyRequest(Controller):

    @route(route='/warranty', auth='user', website=True)
    def warranty_list(self):
        warranty_ids = request.env['product.warranty'].sudo().search([], order='create_date desc')
        return request.render('product_warranty.warranty_tree_view', {
            'warranty_ids': warranty_ids
        })

    @route(route='/form/warranty', auth='user', website=True)
    def warranty(self):
        invoice_ids = request.env['account.move'].search([('move_type', '=', 'out_invoice')])
        return request.render('product_warranty.website_warranty_template',
                              {'invoice_ids': invoice_ids}, )

    @route(route='/warranty/product', auth='user', type='json')
    def product_invoice(self, invoice_id):
        invoice_check = request.env['account.move'].browse(int(invoice_id))
        product_id = invoice_check.mapped('invoice_line_ids.product_id')
        product_ids = request.env['product.product'].search([('has_warranty', '=', True), ('id', 'in', product_id.ids)])
        product_name = product_ids.mapped('name')
        partner_name = invoice_check.partner_id.name
        invoice_date = invoice_check.invoice_date

        return (
            {'product_name': product_name,
             'partner_name': partner_name,
             'invoice_date': invoice_date,
             'product_ids': product_ids.ids,
             })

    @route(route='/change/product', auth='user', type='json')
    def product_change(self, product_id, invoice_date):
        purchase_date = datetime.strptime(invoice_date, '%Y-%m-%d')
        product_check = request.env['product.product'].browse(int(product_id))
        lot_check = request.env['stock.lot'].search([('product_id', 'in', product_check.ids)]).ids
        lot_serial = []
        for i in lot_check:
            lot_serial.append((request.env['stock.lot'].browse(i)).name)
        warranty_period = product_check.warranty_period
        expire_date = purchase_date + timedelta(days=warranty_period)

        return ({
            'lot_id': lot_check,
            'lot_serial': lot_serial,
            'warranty_period': warranty_period,
            'expire_date': expire_date
        })

    @route(route='/create/warranty', auth='user', website=True)
    def create_warranty(self, **kw):
        warranty_id = request.env['product.warranty'].sudo().create({
            'invoice_id': kw.get('invoice_id'),
            'product_id': kw.get('product_id'),
            'lot_serial_id': kw.get('lot_serial'),
            'request_date': kw.get('request_date'),
            'customer_details_id': kw.get('partner'),
            'purchase_date': kw.get('purchase_date'),
            'warranty_expire_date': kw.get('expire_date')

        })
        warranty_id.website_check = True

        return request.render('product_warranty.website_success_warranty_request', {
            'warranty_id': warranty_id
        })

    @route(['''/confirm/warranty<model('product.warranty'):warranty>'''], auth='public', website=True)
    def confirm_warranty(self, warranty):
        warranty_id = request.env['product.warranty'].search([], order='create_date desc')
        warranty.action_submit()
        return request.render('product_warranty.warranty_tree_view', {'warranty_ids': warranty_id})

    @route(['''/view/warranty<model('product.warranty'):warranty>'''], auth='public', website=True)
    def view_confirm_warranty(self, warranty):
        return request.render('product_warranty.website_warranty_view_template', {'warranty': warranty})
