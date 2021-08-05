# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from pytz import timezone, UTC


class PlanningSlot(models.Model):
    _inherit = 'planning.slot'

    allocated_project = fields.Boolean(string="Allocated Department")
    daily_allocated_hours = fields.Float(string="Daily Allocated Hours", compute="compute_daily_allocated_hours",
                                         store=True)

    @api.depends('start_datetime', 'end_datetime', 'allocated_percentage')
    def compute_daily_allocated_hours(self):
        for slot in self:
            if slot.start_datetime and slot.end_datetime and self.env.user.tz:
                if slot.end_datetime > slot.start_datetime:
                    percentage = slot.allocated_percentage / 100.0 or 1
                    start_date = timezone('UTC').localize(slot.start_datetime).astimezone(timezone(self.env.user.tz))
                    end_date = timezone('UTC').localize(slot.end_datetime).astimezone(timezone(self.env.user.tz))
                    end_time_hour = end_date.time().hour
                    end_time_minute = end_date.time().minute
                    start_time_hour = start_date.time().hour
                    start_time_minute = start_date.time().minute
                    difference_hour = int((end_time_hour - start_time_hour))
                    difference_minute = int((end_time_minute - start_time_minute)/0.6)
                    if difference_hour >= 0 and difference_minute >= 0:
                        slot.daily_allocated_hours = float(str(difference_hour)+'.'+str(difference_minute)) * percentage
                    else:
                        slot.daily_allocated_hours = 0.0

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        res = super(PlanningSlot,self)._onchange_employee_id()
        if self.employee_id:
            if self.employee_id.project_id:
                self.project_id = self.employee_id.project_id.id
                self.allocated_project = True
            else:
                self.project_id = False
                self.allocated_project = False
            if self.employee_id.planning_role_id:
                self.role_id = self.employee_id.planning_role_id.id
            else:
                self.role_id = False
        return res