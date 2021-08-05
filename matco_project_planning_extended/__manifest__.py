# -*- coding: utf-8 -*-
{
    'name': "Matco Project Planning Extended",
    'summary': '',
    'description': '',
    'author': "Techultra Solutions",
    'website': "http://www.techultrasolutions.com",
    'category': '',
    'version': '13.0',
    'depends': ['base','planning','project','project_forecast'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/batch_allocation_view.xml',
        'views/planning_slot_view.xml',
        'views/project_reallocation_view.xml',
    ],
}
