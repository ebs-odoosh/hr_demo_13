# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectReallocation(models.Model):
    _name = 'project.reallocation'
    _rec_name = 'employee_id'
    _description = 'Project Reallocation'

    employee_id = fields.Many2one("hr.employee",string="Employee")
    allocated_project_id = fields.Many2one("project.project",string="Allocated Department")
    reallocated_project_id = fields.Many2one("project.project", string="Reallocated Department")
    date_from = fields.Datetime(string="From Date")
    date_to = fields.Datetime(string="To Date")
    planning_slot_id = fields.Many2one("planning.slot",string="Shift")
    overtime_amount = fields.Monetary(string="Overtime Amount")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    reallocated_slot_id = fields.Many2one('planning.slot',string="Reallocated Shift")


    @api.onchange('reallocated_project_id')
    def onchange_reallocated_project(self):
        res = {}
        if self.reallocated_project_id and self.employee_id:
            res['domain'] = {'planning_slot_id': [('project_id', '=', self.reallocated_project_id.id),
                                                  ('role_id', '=', self.employee_id.planning_role_id.id)]}
        return res

    @api.onchange('planning_slot_id')
    def onchange_slot(self):
        if self.planning_slot_id:
            self.date_from = self.planning_slot_id.start_datetime
            self.date_to = self.planning_slot_id.end_datetime


    @api.onchange('employee_id')
    def onchange_allocated_project(self):
        if self.employee_id:
            if self.employee_id.project_id:
                self.allocated_project_id = self.employee_id.project_id.id
            else:
                self.allocated_project_id = False

    @api.model
    def create(self, vals):
        res = super(ProjectReallocation, self).create(vals)
        vals = {
            'employee_id': res.employee_id.id,
            'project_id': res.reallocated_project_id.id,
            'start_datetime': res.date_from,
            'end_datetime': res.date_to,
            'role_id' : res.employee_id.planning_role_id.id
        }
        planning_record = self.env['planning.slot'].create(vals)
        res.write({'reallocated_slot_id' : planning_record.id})
        return res

    def write(self, vals):
        res = super(ProjectReallocation, self).write(vals)
        if self.reallocated_slot_id:
            vals = {
                'employee_id': self.employee_id.id,
                'project_id': self.reallocated_project_id.id,
                'start_datetime': self.date_from,
                'end_datetime': self.date_to,
                'role_id': self.employee_id.planning_role_id.id
                }
            self.reallocated_slot_id.write(vals)
        return res