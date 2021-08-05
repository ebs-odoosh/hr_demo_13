from odoo import api, fields, models, _
from datetime import date


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    project_id = fields.Many2one("project.project", string="Department")
