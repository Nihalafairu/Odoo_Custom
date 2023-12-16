from odoo.http import Controller, request, route


class Partner(Controller):
    @route(route='/Partner', auth='user', website=True)
    def partner(self):
        print("hello", request.env.uid)
        country_ids = request.env['res.country'].search([])
        return request.render('session_website.website_partner_template',
                              {'country_ids': country_ids})

    @route(route="/create/partner", auth='user', website=True)
    def create_partner(self, name, email, **kw):
        # print('create_partner')
        # partner_id = request.env['res.partner'].sudo().create({
        #     'name': name,
        #     'email': email,
        #     'phone': kw.get('phone'),
        #     'city': kw.get('city'),
        #     'country_id': kw.get('country')
        #
        # })
        partner_ids = request.env['res.partner'].sudo().search([], limit=6, order='create_date desc')
        return request.render('session_website.website_success_partner_template',
                              {'partner_id': partner_ids[0],
                               'partner_ids': partner_ids
                               })

    @route(['''/view/partner<model('res.partner'):partner>'''], auth='public', website=True)
    def view_partner(self, partner):
        return request.render('session_website.website_view_partner_template', {'partner': partner})
