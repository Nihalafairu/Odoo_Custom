# -*- coding: utf-8 -*-
from odoo import models, fields


class ContactCreation(models.Model):
    """model used to create contact"""
    _name = "contact.creation"

    survey_id = fields.Many2one('survey.survey')
    title_id = fields.Many2one('survey.question', domain="[('survey_id','=',survey_id)]")
    field_id = fields.Many2one('ir.model.fields', domain="[('model','=','res.partner')]")
