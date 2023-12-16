# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _


class EmployeeHelpdesk(models.Model):
    """model created for employee helpdesk module"""
    _name = "employee.helpdesk"

    _rec_name = 'reference_no'

    reference_no = fields.Char(string='Ticket Reference',
                               readonly=True, default=lambda self: _(''))
    employee_id = fields.Many2one('res.users', string="Employee Name")
    date = fields.Date(default=datetime.today(), readonly=1)
    details = fields.Char(string="Description")
    state = fields.Selection(selection=[
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('reject', 'Rejected'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, default='to_approve')

    def action_approve(self):
        """state changed to approved"""
        self.state = 'approved'

    def action_reject(self):
        """state changed to rejected"""
        self.state = 'reject'

    @api.model
    def create(self, vals):
        """This function is used to create the sequence number"""
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'employee.helpdesk')
        res = super().create(vals)

        return res
