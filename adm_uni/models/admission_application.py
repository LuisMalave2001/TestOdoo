# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from ..utils import formatting


class ApplicationStatus(models.Model):
    _name = "adm_uni.application.status"
    _order = "sequence"


    name = fields.Char(string="Status Name")
    description = fields.Text(string="Description")
    sequence = fields.Integer(readonly=True, default=-1)
    fold = fields.Boolean(string="Fold")
    type = fields.Selection((('stage', "Stage"),
                             ('done', "Done"),
                             ('cancelled', 'Cancelled')),
                            string="Type", default='stage')
    
    partner_id = fields.Many2one("res.partner", string="Customer")
    
    task_ids = fields.Many2many("adm_uni.application.task")

    @api.model
    def create(self, values):
        next_order = self.env['ir.sequence'].next_by_code('sequence.application.task')

        values['sequence'] = next_order
        return super().create(values)


class Application(models.Model):
    _name = "adm_uni.application"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _read_group_status_ids(self,stages,domain,order):
        status_ids = self.env['adm_uni.application.status'].search([])
        return status_ids
    
    # Admission Information
    preferred_degree_program = fields.Many2one("adm_uni.degree_program",
                                               string="Preferred Degree Program")
    
    # Demographic
    name = fields.Char(string="Name", default="Undefined", readonly=True)
    first_name = fields.Char(string="First Name", default="")
    middle_name = fields.Char(string="Middle Name", default="")
    last_name = fields.Char(string="Last Name", default="")
    birthdate = fields.Date(string="Birthdate")
    gender = fields.Selection((('m', 'Male'), ('f', 'Female')), string="Gender")
    father_name = fields.Char("Father name")
    mother_name = fields.Char("Mother name")

    # Contact
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    
    # School
    current_school = fields.Char(string="Current School")
    previous_school = fields.Char(string="Previous School")
    gpa = fields.Float("GPA")
    cumulative_grades = fields.Float("Cumulative Grade")
    regional_exam_grade = fields.Float("Regional Grade")
    bac_grade = fields.Float("BAC Grade")
    
    # Skills
    language_ids = fields.One2many("adm_uni.application.languages", "application_id",
                                    string="Languages")
    
    # Location
    country_id = fields.Many2one("res.country", string="Country")
    state_id = fields.Many2one("res.country.state", string="State")
    city = fields.Char(string="City")
    street_address = fields.Char(string="Street Address")
    zip = fields.Char("zip")
    
    # Documentation
    letter_of_motivation_id =  fields.Many2one("ir.attachment", string="Letter of motivation")
    cv_id =  fields.Many2one("ir.attachment", string="C.V")
    grade_transcript_id =  fields.Many2one("ir.attachment", string="Grade transcript")
    letters_of_recommendation_id =  fields.Many2one("ir.attachment", string="Letter of recommendation")

    # Meta
    contact_time = fields.Many2one("adm_uni.contact_time", 
                                   string="Preferred contact time")
    
    
    status_id = fields.Many2one("adm_uni.application.status",
                                string="Status", group_expand="_read_group_status_ids")
    task_ids = fields.Many2many("adm_uni.application.task")

    state_tasks = fields.Many2many(string="State task", related="status_id.task_ids")

    status_type = fields.Selection(string="Status Type", related="status_id.type")

    def move_to_next_status(self):
        status_ids_ordered = self.env['adm_uni.application.status'].search([], order="sequence")
        index = 0
        for status in status_ids_ordered:
            if status == self.status_id:
                # print("Encontrado! -> {}".format(index))
                break
            index += 1

        index += 1
        if index < len(status_ids_ordered):
            next_status = status_ids_ordered[index]

            # print("Estado actual estado: {}".format(self.status_id.type))
            # print("Siguiente estado: {}".format(next_status.type))
            # print("{} == {} = {}".format(next_status.type, self.status_id.type, self.status_id.type == 'stage'))

            if self.status_id.type == 'done':
                raise exceptions.except_orm(_('Application completed'), _('The Application is already done'))
            elif self.status_id.type == 'cancelled':
                raise exceptions.except_orm(_('Application cancelled'), _('The Application cancelled'))
            else:
                self.status_id = next_status

    def cancel(self):
        status_ids_ordered = self.env['adm_uni.application.status'].search([], order="sequence")
        for status in status_ids_ordered:
            if status.type == 'cancelled':
                self.status_id = status
                break

    @api.onchange("first_name", "middle_name", "last_name")
    def _set_full_name(self):
        self.name = formatting.format_name(self.first_name, self.middle_name, self.last_name) 

    @api.onchange("country_id")
    def _onchange_country_id(self):
        res = {}
        if self.country_id:
            res['domain'] = {'state_id': [('country_id', '=', self.country_id.id)]}

    @api.model
    def create(self, values):
        first_status = self.env['adm_uni.application.status'].search([], order="sequence")[0]
        values['status_id'] = first_status.id
        values['name'] = formatting.format_name(values['first_name'], values['middle_name'], values['last_name']) 
        return super(Application, self).create(values)

    @api.multi
    def write(self, values):

        # print(self.task_ids)
        # print(self.state_tasks)
        #
        # self.condition = ()
        # print(self.condition)

        status_ids = self.env['adm_uni.application.status'].search([])

        print(status_ids)

        if "status_id" in values:
            if not self.state_tasks & self.task_ids == self.state_tasks and self:
                raise exceptions.ValidationError("All task are not completed")

        return super(Application, self).write(values)

    @api.multi
    def unlink(self):
        print("Borrado")
        return super(Application, self).unlink()

    # Mail integration
    # message_follower_ids


class ApplicationTasks(models.Model):
    _name = "adm_uni.application.task"

    name = fields.Char("Name")
    description = fields.Char("Description")

class AdmissionPreferredContactTime(models.Model):
    _name = "adm_uni.contact_time"
    
    name = fields.Char("Name")
    from_time = fields.Float("From Time", compute="_compute_time")
    to_time = fields.Float("To Time", compute="_compute_time")
    
    

class AdmissionLanguages(models.Model):
    _name = "adm_uni.languages"
    
    name = fields.Char("Name")
    
class AdmissionLanguageLevels(models.Model):
    _name = "adm_uni.languages.level"
    
    name = fields.Char("Name")
    
    
class AdmissionApplicationLanguages(models.Model):
    _name = "adm_uni.application.languages"
    
    language_id = fields.Many2one("adm_uni.languages", string="Language")
    language_level_id = fields.Many2one("adm_uni.languages.level", string="Language Level")
    application_id = fields.Many2one("adm_uni.application", string="Application")
    
class AdmissionDegreeProgram(models.Model):
    _name = "adm_uni.degree_program"
    
    name = fields.Char("Name")
    