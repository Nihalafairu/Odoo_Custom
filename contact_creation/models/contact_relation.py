# -*- coding: utf-8 -*-
from odoo import models, fields


class ContactSurvey(models.Model):
    """used to create a new page in survey.survey"""
    _inherit = "survey.survey"

    contact_ids = fields.One2many('contact.creation', 'survey_id')












