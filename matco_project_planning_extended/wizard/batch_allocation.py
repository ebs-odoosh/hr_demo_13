# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
import pytz
from math import ceil, modf
from datetime import datetime, timedelta

class BatchAllocation(models.TransientModel):
    _name = "batch.allocation"
    _description = "Batch Allocation"

    def _default_start_datetime(self):
        return fields.Datetime.to_string(datetime.combine(fields.Datetime.now(), datetime.min.time()))

    def _default_end_datetime(self):
        return fields.Datetime.to_string(datetime.combine(fields.Datetime.now(), datetime.max.time()))

    project_id = fields.Many2one('project.project',string="Department")
    role_id = fields.Many2one('planning.role',string="Role")
    employee_ids = fields.Many2many('hr.employee',string="Employee")
    template_id = fields.Many2one('planning.slot.template', string='Shift Template')
    start_datetime = fields.Datetime(string="Start Datetime",default=_default_start_datetime)
    end_datetime = fields.Datetime(string="End Datetime",default=_default_end_datetime)
    allocated_project = fields.Boolean(string="Allocated")

    @api.onchange('template_id')
    def _onchange_template_id(self):
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
        if self.template_id and self.start_datetime:
            h = int(self.template_id.start_time)
            m = round(modf(self.template_id.start_time)[0] * 60.0)
            start = pytz.utc.localize(self.start_datetime).astimezone(user_tz)
            start = start.replace(hour=int(h), minute=int(m))
            self.start_datetime = start.astimezone(pytz.utc).replace(tzinfo=None)
            h = int(self.template_id.duration)
            m = round(modf(self.template_id.duration)[0] * 60.0)
            delta = timedelta(hours=int(h), minutes=int(m))
            self.end_datetime = fields.Datetime.to_string(self.start_datetime + delta)

            if self.template_id.role_id:
                self.role_id = self.template_id.role_id



    @api.onchange('project_id')
    def onchange_project(self):
        if self.project_id:
            if self.role_id:
                employee_ids = self.env['hr.employee'].search(
                    [('planning_role_id', '=', self.role_id.id),
                     ('project_id', '=', self.project_id.id),
                     ('company_id', '=', self.env.company.id)])
            else:
                employee_ids  = self.env['hr.employee'].search(
                    [('project_id', '=', self.project_id.id),
                     ('company_id', '=', self.env.company.id)])
            if employee_ids:
                self.employee_ids = employee_ids
            else:
                self.employee_ids = False
        else:
            self.employee_ids = False


    @api.onchange('role_id')
    def onchange_structure(self):
        if self.role_id:
            if self.project_id:
                employee_ids = self.env['hr.employee'].search(
                    [('planning_role_id', '=', self.role_id.id),
                     ('project_id', '=', self.project_id.id),
                     ('company_id', '=', self.env.company.id)])
            else:
                employee_ids = self.env['hr.employee'].search(
                    [('planning_role_id', '=', self.role_id.id),
                     ('company_id', '=', self.env.company.id)])
            self.employee_ids = employee_ids
        elif not self.project_id:
            self.employee_ids = False
        else:
            self.onchage_project()

    def create_shift(self):
        if self.employee_ids:
            for employee in self.employee_ids:
                vals = {
                    'employee_id': employee.id,
                    'project_id': self.project_id.id,
                    'role_id': self.role_id.id,
                    'start_datetime': self.start_datetime,
                    'end_datetime': self.end_datetime
                }
                if self.allocated_project:
                    vals.update({'allocated_project': True})
                record = self.env['planning.slot'].create(vals)

