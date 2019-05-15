from odoo import models, fields

class CmkFacturation(models.Model):
    _inherit = 'account.invoice'

    is_patient = fields.Boolean(string='Est un patient')