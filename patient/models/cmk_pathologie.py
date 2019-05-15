# -*- coding: utf-8 -*-

from odoo import models, fields

class CmkPathologie(models.Model):
    _name = 'cmk.pathologie'
    #_inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom de la pathologie')
    prix = fields.Integer(string='Prix')
    id = fields.Integer(string='Id')
    pathologie = fields.Text(string='Description')
    note = fields.Text(string='Note')
