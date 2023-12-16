from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class Bom(WebsiteSale):
    @route('/shop/cart', type='http', auth='public', website=True)
    def cart(self, access_token=None, revive='', **post):
        res = super(Bom, self).cart(access_token=access_token, revive=revive, **post)
        orders = request.website.sale_get_order()
        get_param = request.env['ir.config_parameter'].sudo().get_param
        product_ids = get_param('bom_cart.product_ids')
        product_id = product_ids[1:-1]
        if product_id:
            x = product_id.split(", ")
            products = []
            for i in x:
                products.append(int(i))
            pro_check = request.env['product.product'].search([('id', 'in', products)])
            product_check = pro_check.ids

            res.qcontext['product'] = product_check

        return res

    @route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(
            self, product_id, line_id=None, add_qty=None, set_qty=None, display=True,
            product_custom_attribute_values=None, no_variant_attribute_values=None, **kw
    ):
        res = super(Bom, self).cart_update_json(product_id=product_id, line_id=line_id, add_qty=add_qty,
                                                set_qty=set_qty, display=display,
                                                product_custom_attribute_values=product_custom_attribute_values,
                                                no_variant_attribute_values=no_variant_attribute_values, **kw)

        orders = request.website.sale_get_order()
        get_param = request.env['ir.config_parameter'].sudo().get_param
        product_ids = get_param('bom_cart.product_ids')
        product_id = product_ids[1:-1]
        print(product_id)
        if product_id:
            x = product_id.split(", ")
            products = []
            for i in x:
                products.append(int(i))
            pro_check = request.env['product.product'].search([('id', 'in', products)])
            product_check = pro_check.ids
            res['product'] = product_check
        return res
