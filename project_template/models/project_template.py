from odoo import models, fields


class ProjectTemplate(models.Model):
    """this model is used to create project template"""
    _name = "project.template"

    name = fields.Char(string="Name", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    tag_ids = fields.Many2many('project.tags', string="Tags")
    company_id = fields.Many2one('res.company', string="Company")
    project_manager_id = fields.Many2one('res.users', string="Project Manager")
    description = fields.Html()
    planned_date = fields.Date
    privacy_visibility = fields.Selection(string="Visibility", selection=[('followers','Invited internal users'),('employees', 'All internal Usres'),('portal', 'Invited portal users and all internal users')])

    def action_create(self):
        """this function is used to create new project when Create Project button is clicked"""
        name = self.name
        record = self.env['project.project'].create({
            'name': name,
            'partner_id': self.customer_id.id,
            'tag_ids': self.tag_ids
        })
        return record.id





