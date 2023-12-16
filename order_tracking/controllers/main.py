from odoo.http import Controller, request, route


class OrderTracking(Controller):
    @route(route='/tracking', auth='user', website=True)
    def order_tracking(self):
        order_ids = request.env['sale.order'].search([])
        return request.render('order_tracking.website_tracking_order_view', {
            'order_ids': order_ids
        })

    @route(['''/view/tracking<model('sale.order'):order>'''], auth='public', website=True)
    def view_tracking(self, order):
        return request.render('order_tracking.website_tracking_view', {'tracking': order.picking_ids.track_ids})

