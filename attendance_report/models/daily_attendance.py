# -*- coding: utf-8 -*-
from odoo import models, fields


class DailyAttendance(models.Model):
    """created to get the details of day wise attendance"""
    _name = "daily.attendance"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    employee_mail = fields.Char(related='employee_id.work_email')
    employee_department_id = fields.Many2one(related='employee_id.department_id')
    check_in = fields.Date(string="Check in")

    def daily_attendance(self, ):
        """Created the day wise attendance details"""
        attendance_list = self.env['hr.attendance'].search([])
        for attendance in attendance_list:
            employee_id = attendance.employee_id
            self.env['daily.attendance'].create({
                'employee_id': employee_id.id,
                'employee_mail': employee_id.work_email,
                'employee_department_id': employee_id.department_id,
                'check_in': attendance.check_in.date()
            })

