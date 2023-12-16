# -*- coding: utf-8 -*-

from odoo.http import request, route
from odoo.addons.survey.controllers.main import Survey


class Contact(Survey):
    @route('/survey/submit/<string:survey_token>/<string:answer_token>', type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        """ when survey is submitted a new contact is created """
        res = super(Contact, self).survey_submit(survey_token=survey_token, answer_token=answer_token, **post)
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']
        survey = request.env['survey.user_input.line'].search([('survey_id', '=', survey_sudo.id)],
                                                              order="create_date desc",
                                                              limit=1)
        questions = request.env['survey.question'].search([('id', '=', survey.question_id.id)])
        answers = survey.value_char_box
        contact = ''
        fields = request.env['contact.creation'].search([('title_id', '=', questions.id)]).field_id
        ans = {'field_name': fields.name, 'answer': answers}
        if ans['field_name'] == 'name':
            if ans['answer'] != 'skipped':
                contact = request.env['res.partner'].create({
                    ans['field_name']: ans['answer']

                })
        else:
            contact = request.env['res.partner'].search([], order="create_date desc", limit=1)
            contact.write({
                ans['field_name']: ans['answer']

            })

        return res
