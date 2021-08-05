# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from datetime import date,datetime,timedelta
from ast import literal_eval
import datetime
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta

class BtHrOvertime(models.Model):   
    _name = "bt.hr.overtime"
    _description = "Bt Hr Overtime" 
    _rec_name = 'employee_id'
    _order = 'id desc'
    
    employee_id = fields.Many2one('hr.employee', string="Employee")
    manager_id = fields.Many2one('hr.employee', string='Manager')
    start_date = fields.Datetime('Date')
    overtime_hours = fields.Float('Overtime Hours')
    notes = fields.Text(string='Notes')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Waiting Approval'), ('refuse', 'Refused'), 
           ('validate', 'Approved'), ('cancel', 'Cancelled')], default='draft', copy=False)
    attendance_id = fields.Many2one('hr.attendance', string='Attendance')
    user_id = fields.Many2one('res.users', string="Responsible")


    @api.model
    def run_overtime_scheduler(self):
        """ This Function is called by scheduler. """
        attend_signin_ids = self.env['hr.attendance'].search([('overtime_created', '=', False)])
        for obj in attend_signin_ids:
            if obj.check_in and obj.check_out:
                start_date = datetime.datetime.strptime(obj.check_in.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATETIME_FORMAT)
                end_date = datetime.datetime.strptime(obj.check_out.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATETIME_FORMAT)
                difference = end_date - start_date
                #To calculate hour difference of an employee. It will calculate hour difference even if employee work more than 24 hours
                hour_diff =int((difference.days) * 24 + (difference.seconds) / 3600)
                min_diff = str(difference).split(':')[1]
                tot_diff = str(hour_diff) + '.' + min_diff
                actual_working_hours = float(tot_diff)
                planning_slot = self.env['planning.slot'].search([('employee_id', '=', obj.employee_id.id),('project_id', '=', obj.project_id.id),('allocated_project', '=', True)], limit=1)
                if planning_slot:
                    if actual_working_hours > planning_slot.daily_allocated_hours:
                        overtime_hours = actual_working_hours - planning_slot.daily_allocated_hours
                        vals = {
                            'employee_id':obj.employee_id and obj.employee_id.id or False,
                            'manager_id' : obj.employee_id and obj.employee_id.parent_id and obj.employee_id.parent_id.id or False,
                            'start_date' : obj.check_in,
                            'overtime_hours': round(overtime_hours,2),
                            'attendance_id': obj.id,
                            'user_id': obj.project_manager_id.id if obj.project_manager_id.id else False
                            }
                        record = self.env['bt.hr.overtime'].create(vals)
                        # overtime_record.append(record)
                        obj.overtime_created = True
                elif obj.project_id:
                    if obj.project_id != obj.employee_id.project_id:
                        vals = {
                            'employee_id': obj.employee_id and obj.employee_id.id or False,
                            'manager_id': obj.employee_id and obj.employee_id.parent_id and obj.employee_id.parent_id.id or False,
                            'start_date': obj.check_in,
                            'overtime_hours': round(actual_working_hours, 2),
                            'attendance_id': obj.id,
                            'user_id': obj.project_manager_id.id if obj.project_manager_id.id else False
                        }
                        record = self.env['bt.hr.overtime'].create(vals)
                        # overtime_record.append(record)
                        obj.overtime_created = True





    # @api.model
    # def run_overtime_scheduler(self):
    #     """ This Function is called by scheduler. """
    #     current_date = date.today()
    #     working_hours_empl = self.env['hr.contract']
    #     attend_signin_ids = self.env['hr.attendance'].search([('overtime_created', '=', False)])
    #     for obj in attend_signin_ids:
    #         if obj.check_in and obj.check_out:
    #             start_date = datetime.datetime.strptime(obj.check_in.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATETIME_FORMAT)
    #             end_date = datetime.datetime.strptime(obj.check_out.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATETIME_FORMAT)
    #             difference = end_date - start_date
    #             #To calculate hour difference of an employee. It will calculate hour difference even if employee work more than 24 hours
    #             hour_diff =int((difference.days) * 24 + (difference.seconds) / 3600)
    #             min_diff = str(difference).split(':')[1]
    #             tot_diff = str(hour_diff) + '.' + min_diff
    #             actual_working_hours = float(tot_diff)
    #             contract_obj = self.env['hr.contract'].search([('employee_id', '=', obj.employee_id.id),('work_hours','!=',0)])
    #             for contract in contract_obj:
    #                 working_hours = contract.work_hours
    #                 if actual_working_hours > working_hours:
    #                     overtime_hours = actual_working_hours - working_hours
    #                     vals = {
    #                         'employee_id':obj.employee_id and obj.employee_id.id or False,
    #                         'manager_id' : obj.employee_id and obj.employee_id.parent_id and obj.employee_id.parent_id.id or False,
    #                         'start_date' : obj.check_in,
    #                         'overtime_hours': round(overtime_hours,2),
    #                         'attendance_id': obj.id,
    #                         }
    #                     self.env['bt.hr.overtime'].create(vals)
    #                     obj.overtime_created = True
                        
    def action_submit(self):
        return self.write({'state':'confirm'})
            
    def action_cancel(self):
        return self.write({'state':'cancel'})
            
    def action_approve(self):
        return self.write({'state':'validate'})
        
    def action_refuse(self):
        return self.write({'state':'refuse'})
            
    def action_view_attendance(self):
        attendances = self.mapped('attendance_id')
        action = self.env.ref('hr_attendance.hr_attendance_action').read()[0]
        if len(attendances) > 1:
            action['domain'] = [('id', 'in', attendances.ids)]
        elif len(attendances) == 1:
            action['views'] = [(self.env.ref('hr_attendance.hr_attendance_view_form').id, 'form')]
            action['res_id'] = self.attendance_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
        

class Contract(models.Model):
    _inherit = 'hr.contract'
    
    work_hours = fields.Float(string='Working Hours')
    
    
class HrAttendance(models.Model):
    _inherit = "hr.attendance" 
    
    overtime_created = fields.Boolean(string = 'Overtime Created', default=False, copy=False)
