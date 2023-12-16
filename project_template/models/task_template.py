from odoo import models, fields


class TaskTemplate(models.Model):
    """This model is used to create Task Templates"""
    _name = "task.template"

    name = fields.Char(string="Task Title", required=True)
    project_id = fields.Many2one('project.project', string="Project", required=True)
    assignees_ids = fields.Many2many('res.users', string="Assignees")
    customer_id = fields.Many2one('res.partner', string="Customer")
    tag_ids = fields.Many2many('project.tags', string="Tags")
    milestone_id = fields.Many2one('project.task', string="Milestone")
    sale_line_id = fields.Many2one('sale.order.line', string="Sale Order Item")
    deadline = fields.Date(string="Deadline")
    company_id = fields.Many2one('res.company', string="Company")
    sequence = fields.Integer(string="Sequence")
    email_cc = fields.Char(string="Email cc")
    description = fields.Html(string="Description")
    parent_id = fields.Many2one('task.template')
    child_ids = fields.One2many('task.template', 'parent_id')
    task_ids = fields.One2many('project.task','template_id')
    task_id = fields.Many2one('project.task')

    def action_create_task(self):
        """Task is created when Create Task button is clicked"""
        main_task = self.env['project.task'].create({
            'name': self.name,
            'user_ids': self.assignees_ids,
            'project_id': self.project_id.id,
            # 'child_ids': self.task_ids

        })
        self.task_id = main_task
        for child in self.child_ids:
            self.create_task(child.id, main_task)

    def create_task(self, task_id, sub):
        """sub task is also created from the template"""
        task = self.browse(task_id)
        sub_task = self.env['project.task'].create({
            'name': task.name,
            'user_ids': task.assignees_ids,
            'project_id': task.project_id.id,
            'parent_id': sub.id
        })
        self.task_id = sub_task
        if task.child_ids:
            for child in task.child_ids:
                return self.create_task(child.id, sub_task)
        else:
            return



