from odoo import http
from odoo.http import request


class WarrantySnippet(http.Controller):
    @http.route(['/warranty/snippet'], auth='user', type='json')
    def warranty_snippet(self):
        warranty_id = request.env['product.warranty'].search([('website_check', '=', True)])
        warranty_list = []
        for i in warranty_id:
            warranty_list.append({
                'invoice_id': i.invoice_id.name,
                'product': i.product_id,

                'product_tmpl_id': i.product_id.product_tmpl_id.id,
                'product_id': i.product_id.id,
                'product_name': i.product_id.name,
                'warranty_expire_date': i.warranty_expire_date,
                'product_image': i.product_image,
                'id': i.id,

            })
        return warranty_list

    @http.route(['''/view/warranty<model('product.warranty'):warranty>'''], auth='public', website=True)
    def view_confirm_warranty(self, warranty):
        return request.render('product_warranty.website_warranty_view_template', {'warranty': warranty})

    @http.route(['''/view/snippet/<int:id>'''], auth='public', website=True)
    def view_snippet_warranty(self, id):
        warranty = request.env['product.warranty'].browse(id)
        return request.render('product_warranty.website_warranty_view_template', {'warranty': warranty})

