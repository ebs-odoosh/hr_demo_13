{
    'name': 'Matco HR Attendance Portal',
    'version': '13.0',
    'summary': 'Manage HR Attendance Portal',
    'description': """
        """,
    'category': '',
    'author': "",
    'company': 'Techultra Solutions Pvt. Ltd.',
    'maintainer': '',
    'website': "",
    'depends': ['website', 'project','hr_timesheet','hr'],
    'data': [
        'data/attendance_menu.xml',
        'views/attendance_webpage.xml',
        'views/attendance_inherit_view.xml',
        'views/hr_employee_view.xml',
    ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
