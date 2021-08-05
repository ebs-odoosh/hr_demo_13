# -*- coding: utf-8 -*-
{
    'name': 'Automatic Overtime Calculation',
    'summary': 'Automatic Overtime Calculation',
    'version':'0.1',
    'license':'AGPL-3',
    'description': """
    Management of overtime taken by the employees.
""",
    'category': 'Generic Modules/Human Resources',
    'author' : 'Techultra Solutions Pvt. Ltd.',
    'website': '',
    'depends':['hr_contract','hr_attendance','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/bt_hr_overtime_view.xml',
        'data/bt_hr_overtime_data.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
    'application': True,
}



# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
