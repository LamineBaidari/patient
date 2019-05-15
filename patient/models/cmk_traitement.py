# -*- coding: utf-8 -*-

from odoo import models, fields

class CmkTraitement(models.Model):
    _name = 'cmk.traitement'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string='Nom du traitement')
    id = fields.Integer(string='Id')
    montant = fields.Integer(string='Coût') 
    traitement = fields.Text(string='Description')
    notes = fields.Text(string='Note')
    
    date_seance = fields.Date(string='Date de la séance de traitement')
    kine_assigne = fields.Many2one('hr.employee', string='Kiné traitant')
    duree_seance = fields.Float(string='Durée de la séance')
    presence_patient = fields.Selection( [
        ('oui', "Oui"), ('non', "Non")
    ], string='Présent ?')

    patient_traitement = fields.Many2one('cmk.patient', string="Patient") #c'est le patient