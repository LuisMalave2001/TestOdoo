# -*- coding: utf-8 -*-
from odoo import http
from ..utils import formatting
import base64


def get_parameters():
    return http.request.httprequest.args


def post_parameters():
    return http.request.httprequest.form


class Admission(http.Controller):

    #===================================================================================================================
    # @http.route("/")
    # def
    #===================================================================================================================

    @http.route("/admission-university/inquiry", auth="public", methods=["GET"], website=True)
    def admission_web(self):
        countries = http.request.env['res.country']
        contact_times = http.request.env['adm_uni.contact_time']
        degree_programs = http.request.env['adm_uni.degree_program']

        response = http.request.render('adm_uni.template_admission', {
            'countries': countries.search([]),
            'contact_times': contact_times.search([]),
            'degree_programs': degree_programs.search([]),
        })
        return response

    @http.route("/admission-university/inquiry", auth="public", methods=["POST"], website=True, csrf=False)
    def add_admission(self, **params):
        if "txtMiddleName" not in params:
            params["txtMiddleName"] = ""
            
        # Personal Info
        first_name = params["txtFirstName"]
        last_name = params["txtLastName"]
        middle_name = params["txtMiddleName"]
        birthdate = params["txtBirthdate"]
        gender = params["selGender"]
        father_name = params["txtFatherName"]
        mother_name = params["txtMotherName"]
        
        # Contact
        email = params["txtEmail"]
        phone = params["txtHomePhone"]
        
        # School information
        current_school = params["txtCurrentSchool"]
        previous_school = params["txtPreviousSchool"]
        gpa = params["txtGPA"]
        cumulative_grades = params["txtCumulativeGrade"]
        regional_exam_grade = params["txtRegionalExam"]
        bac_grade = params["txtBACGrade"]
        
        # Location
        country = params["selCountry"]
        state = params["selState"] if params["selState"] != "-1" else False
        city = params["txtCity"]
        street_address = params["txtStreetAddress"]
        zipCode = params["txtZip"]
        
        # Documentation 
        letter_of_motivation_file = params["fileLetterOfMotivation"]
        cv_file = params["fileCV"]
        grade_transcript_file = params["fileGradeTranscript"]
        letters_of_recommendation_file = params["fileLettersOfRecommendation"]
        
        
        new_student_dict = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'birthdate': birthdate,
            'gender': gender,
            'father_name': father_name,
            'mother_name': mother_name,
            
            'email': email,
            'phone': phone,
            
            'current_school': current_school,
            'previous_school': previous_school,
            'gpa': gpa,
            'cumulative_grades': cumulative_grades,
            'regional_exam_grade': regional_exam_grade,
            'bac_grade': bac_grade,

            'country_id': country,
            'state_id': state,
            'city': city,
            'street_address': street_address,
            'zip': zipCode,
            
            #===========================================================================================================
            # 'letter_of_motivation_id': letter_of_motivation_id,
            # 'cv_id': cv_id,
            # 'grade_transcript_id': grade_transcript_id,
            # 'letters_of_recommendation_id': letters_of_recommendation_id,
            #===========================================================================================================

            # 'contact_time': contact_time,
        }
        
        InquiryEnv = http.request.env["adm_uni.inquiry"]
        student = InquiryEnv.create(new_student_dict)

        AttachmentEnv = http.request.env["ir.attachment"]
        motivation_id = AttachmentEnv.sudo().create({
            'name': letter_of_motivation_file.filename,
            'datas_fname': letter_of_motivation_file.filename,
            'res_name': letter_of_motivation_file.filename,
            'type': 'binary',   
            'res_model': 'adm_uni.inquiry',
            'res_id': student.id,
            'datas': base64.b64encode(letter_of_motivation_file.read()),
        })
        cv_id = AttachmentEnv.sudo().create({
            'name': cv_file.filename,
            'datas_fname': cv_file.filename,
            'res_name': cv_file.filename,
            'type': 'binary',   
            'res_model': 'adm_uni.inquiry',
            'res_id': student.id,
            'datas': base64.b64encode(cv_file.read()),
        })
        grade_transcript_id = AttachmentEnv.sudo().create({
            'name': grade_transcript_file.filename,
            'datas_fname': grade_transcript_file.filename,
            'res_name': grade_transcript_file.filename,
            'type': 'binary',   
            'res_model': 'adm_uni.inquiry',
            'res_id': student.id,
            'datas': base64.b64encode(grade_transcript_file.read()),
        })
        letters_of_recommendation_id = AttachmentEnv.sudo().create({
            'name': letters_of_recommendation_file.filename,
            'datas_fname': letters_of_recommendation_file.filename,
            'res_name': letters_of_recommendation_file.filename,
            'type': 'binary',   
            'res_model': 'adm_uni.inquiry',
            'res_id': student.id,
            'datas': base64.b64encode(letters_of_recommendation_file.read()),
        })
        
        student.letter_of_motivation_id = motivation_id
        student.cv_id = cv_id
        student.grade_transcript_id = grade_transcript_id
        student.letters_of_recommendation_id = letters_of_recommendation_id

        
        return "Exito, se ha enviado el estudiante: '{}'".format(student.name)
