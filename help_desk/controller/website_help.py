from odoo.http import Controller, request, route


class Helpdesk(Controller):
    """helpdesk details in website """

    @route(route='/helpdesk', auth='user', website=True)
    def helpdesk(self):
        """help desk tree view is opened when employee is logged in"""
        help_desk = request.env['employee.helpdesk'].search([('create_uid', '=', request.env.user.id)])
        return request.render('help_desk.helpdesk_tree_view', {
            'helpdesk_ids': help_desk
        })

    @route(route='/form/helpdesk', auth='user', website=True)
    def helpdesk_form(self):
        """helpdesk form is opened when create button is pressed"""
        return request.render('help_desk.website_helpdesk_template')

    @route(route="/create/helpdesk", auth='user', website=True)
    def create_help(self, **kw):
        """ created ticket through website"""
        help_desk = request.env['employee.helpdesk'].search([], order="create_date desc", limit=1)
        if request.env.user.has_group('help_desk.helpdesk_user_access'):
            helpdesk_id = request.env['employee.helpdesk'].sudo().create({
                'employee_id': request.env.user.id,
                'details': kw.get('help')

            })

            return request.render('help_desk.website_success_helpdesk',
                                  {'helpdesk_id': helpdesk_id,
                                   'help_desk': help_desk
                                   })
