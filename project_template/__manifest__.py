{
    'name': "Project Template",
    'version': '16.0.1.1.1',
    'category': 'project_template',
    'depends': ['base','project','sale'],
    'author': "Nihala",
    'description': "This app allows your project team to create project template and task template",
    'data': [
        'security/ir.model.access.csv',
        'views/project_template_view.xml',
        'views/task_template_view.xml',
        'views/reverse_project_view.xml',
        'views/reverse_task_view.xml',
        'views/project_menu_action.xml',
    ],

    'installable': True
}
