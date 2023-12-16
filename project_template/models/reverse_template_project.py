from odoo import models


class ReverseTemplate(models.Model):
    _inherit = 'project.project'

    def action_create_template(self):
        """project template is created from project"""
        project_template = self.env['project.template'].create({
            'name': self.name,
            'customer_id': self.partner_id.id,
            'tag_ids': self.tag_ids
        })
        return project_template

