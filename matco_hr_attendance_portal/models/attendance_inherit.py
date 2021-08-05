from odoo import models, fields, api, exceptions, _


class HrAttendanceInherit(models.Model):
    _inherit = "hr.attendance"

    project_manager_id = fields.Many2one("res.users", string="Department Manager")
    project_id = fields.Many2one("project.project", string="Department")
    present_absent = fields.Selection([
        ('late', 'Late'),
        ('absent', 'Absent'),
        ('attended', 'Attended')], string='Attendance')
    days = fields.Float(string='Days')

    # call method from rpc
    def get_number_of_days(self):
        pass




class AccountAnalyticLineInherit(models.Model):
    _inherit = "account.analytic.line"

    project_manager_id = fields.Many2one("res.users", string="Project Manager")
    # project_id = fields.Many2one("project.project", string="Project")
    present_absent = fields.Selection([
        ('late', 'Late'),
        ('absent', 'Absent'),
        ('attended', 'Attended')], string='Attendance')
    days = fields.Float(string='Days')


