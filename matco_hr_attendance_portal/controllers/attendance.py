# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime,timedelta
from pytz import timezone
import pytz

class Attendance(http.Controller):

    @http.route(['/attendance/planning_slot'], type='json', auth="public", methods=['POST'], website=True)
    def get_planning_slot(self, **kwargs):
        if kwargs.get('employee_id') not in ['none', None] and kwargs.get('project_id') not in ['none', None]:
            employee = request.env['hr.employee'].browse(kwargs.get('employee_id'))
            project = request.env['project.project'].browse(kwargs.get('project_id'))
            if employee.project_id == project:
                employee_shift = request.env['planning.slot'].search([('allocated_project', '=', True),
                                                                      ('employee_id', '=', employee.id),
                                                                      ('project_id', '=', project.id)])
                if employee_shift:
                    start_date = timezone('UTC').localize(employee_shift.start_datetime).astimezone(timezone(request.env.user.tz))
                    end_date = timezone('UTC').localize(employee_shift.end_datetime).astimezone(timezone(request.env.user.tz))

                    return {'start_datetime': start_date.strftime("%m/%d/%Y %I:%M %p"),
                            'end_datetime': end_date.strftime("%m/%d/%Y %I:%M %p")}
                else:
                    return False
            else:
                employee_shift = request.env['planning.slot'].search([('allocated_project', '=', False),
                                                                      ('employee_id', '=', employee.id),
                                                                      ('project_id', '=', project.id)])
                if employee_shift:
                    start_date = timezone('UTC').localize(employee_shift.start_datetime).astimezone(timezone(request.env.user.tz))
                    end_date = timezone('UTC').localize(employee_shift.end_datetime).astimezone(timezone(request.env.user.tz))
                    return {'start_datetime': start_date.strftime("%m/%d/%Y %I:%M %p"),
                            'end_datetime': end_date.strftime("%m/%d/%Y %I:%M %p")}
                else:
                    return False



    @http.route('/attendance', type='http', auth='public', website=True, )
    def render_attendance_page(self, **kw):

        if request.env.user.has_group('project.group_project_manager'):

            project_ids = request.env['project.project'].sudo().search([('user_id', '=', request.env.user.id)])
            value = {
                'project_ids': project_ids,
            }
            return http.request.render('matco_hr_attendance_portal.attendance_web_page', value)
        else:
            return http.request.render('matco_hr_attendance_portal.excess_page', {})

    @http.route(['/attendance/employee'], type='json', auth="public", methods=['POST'], website=True)
    def get_attendance_employee(self, **kwargs):
        employee_dict = {}
        task_dict = {}
        if kwargs.get('id') not in ['none', None]:
            project_id = request.env['project.project'].sudo().browse(kwargs.get('id'))
            # employee = request.env['hr.employee'].sudo().search([('project_id', '=', project_id.id)])
            # employees = request.env['hr.employee'].sudo().search([('project_id', '=', project_id.id)])
            employees = request.env['planning.slot'].sudo().search([('project_id','=',project_id.id)]).mapped('employee_id')

            # employees = request.env['hr.employee'].sudo().browse(employee_ids)
            for employee in employees:
                employee_dict.update({employee.id: employee.name})
            task = request.env['project.task'].sudo().search([('project_id', '=', project_id.id)])
            for rec in task:
                task_dict.update({rec.id: rec.name})
        return {'employee_id': employee_dict, 'task_id': task_dict}

    @http.route('/attendance/information', type='http', auth='public', website=True, csrf_token=False)
    def navigate_to_information_page(self, **kwargs):
        if kwargs.get('employee'):
            utc = pytz.timezone('UTC')
            user_tz = pytz.timezone(request.env.user.tz or 'UTC')
            hours_utc = datetime.now(utc).hour-datetime.now(user_tz).hour
            minutes_utc = datetime.now(utc).minute-datetime.now(user_tz).minute
            start_date = datetime.strptime(kwargs.get('start_date'), "%m/%d/%Y %I:%M %p")
            start_date = start_date+timedelta(hours=hours_utc,minutes=minutes_utc)
            end_date = datetime.strptime(kwargs.get('date_end'), "%m/%d/%Y %I:%M %p")
            end_date = end_date + timedelta(hours=hours_utc, minutes=minutes_utc)
            request.env['hr.attendance'].sudo().create({
                'project_manager_id': request.env.user.id,
                'project_id': kwargs.get('project'),
                'employee_id': kwargs.get('employee'),
                'present_absent': kwargs.get('present_absent'),
                'days': kwargs.get('days'),
                'check_in': start_date,
                'check_out': end_date,
            })

            if kwargs.get('project_task') != None:
                task = int(kwargs.get('project_task'))
            else:
                # task=kwargs.get('new_task')
                task_id = request.env['project.task'].sudo().create({
                    'name': kwargs.get('new_task'),
                    'project_id': int(kwargs.get('project')),
                    'user_id': request.env.user.id,
                })

                task = task_id.id
            # request.env['account.analytic.line'].sudo().create({
            #     'project_manager_id': request.env.user.id,
            #     'project_id': int(kwargs.get('project')),
            #     'task_id': task,
            #     'employee_id': int(kwargs.get('employee')),
            #     'present_absent': kwargs.get('present_absent'),
            #     'days': kwargs.get('days'),
            #     'unit_amount': kwargs.get('from_to_time'),
            #     # 'check_in': datetime.strptime(kwargs.get('start_date'), ""%m/%d/%Y %I:%M %p"),
            #     # 'check_out': datetime.strptime(kwargs.get('date_end'), "%m/%d/%Y %I:%M %p"),
            # })
        return http.request.render('matco_hr_attendance_portal.information_page', {})
