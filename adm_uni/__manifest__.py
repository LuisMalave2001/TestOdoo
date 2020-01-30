# -*- coding: utf-8 -*-

{
    'name': "Admission University",

    'summary': """""",

    'description': """""",

    'author': "Eduweb Group SL",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Admission',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'school_base', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views_inquiry.xml',
        'views/views_application.xml',
        'data/menudata.xml',
        'data/sequences_data.xml',
        'data/statics_data.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}

