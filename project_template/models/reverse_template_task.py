from odoo import models, fields


class ReverseTemplateTask(models.Model):
    _inherit = 'project.task'

    template_id = fields.Many2one('task.template')

    def action_create_task_template(self):
        """task template is created from the task"""
        main_task_template = self.env['task.template'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'assignees_ids': self.user_ids,
            'task_ids': self.child_ids,
        })
        self.template_id = main_task_template
        for child in self.child_ids:
            self.create_task_template(child.id, main_task_template)

    def create_task_template(self, template_id, task_template):
        """task template is created from the subtask """
        task = self.browse(template_id)
        sub_task_template = self.env['task.template'].create({
            'name': task.name,
            'project_id': task.project_id.id,
            'assignees_ids': task.user_ids,
            'task_ids': task.child_ids,
            'parent_id': task_template.id
        })
        self.template_id = sub_task_template
        if task.child_ids:
            for child in task.child_ids:
                return self.create_task_template(child.id, sub_task_template)
        else:
            return
