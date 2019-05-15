###################################################################################
#
#    Enablis - Carrefour
#    Copyright (C) 2019
#    Author: Omizuka, Rodolphe_ci & Aziz
#    Company: 
#
###################################################################################
# -*- coding: utf-8 -*-
{
    'name': "Patient",
    'summary': """Module de gestion des patients""",
    'description': """
        Ce module est le module principal de Chez Mon Kiné.
        Il permettra la gestion des patients, des kiné et des rendez-vous.
    """,
    'author': "Omizuka, Rodolphe_ci & Aziz",
    #'license': "AGPL-3",
    'maintainer': "Omizuka, Rodolphe_ci & Aziz",
    #'website': "http://www.yourcompany.com",
    'category': 'Enablis',
    'version': '0.1',
    'depends': ['base', 'hr', 'account', 'mail'],
    'data': [
        'security/cmk_security.xml',
        'security/ir.model.access.csv',
        'views/cmk_patient_vue.xml',
        'views/pathologies.xml',
        'views/traitements.xml',
        #'views/cmk_patient_suivitraitement_vue.xml',
        #'views/facturation_menu.xml',
        'views/cmk_facturation_vue.xml',
    ],
    'application': True,
    'auto_install': False,
    'installable':True,
    'images': ['static/icon.png'],

}