# -*- coding: utf-8 -*-

from ast import literal_eval
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _

CHAMPS_ADRESSES = ('adresse_rue', 'adresse_ville', 'adresse_pays', 'adresse_postal')

class CmkPatient(models.Model):
    _name = 'cmk.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    #_inherit = 'res.partner'
    #_rec_name = 'patient'
    _description = 'Patient'

    #code patient (identifiant) généré automatiquement pour le patient
    id_patient = fields.Char(string='Numéro d\'identification', size=16, readonly=True,
        help="Code patient (identifiant) généré automatiquement", default=lambda *a: 'PATXXXX')
    #id_patient = fields.Char(string='Code patient', required=True, copy=False,
    #readonly=True, index=True, default=lambda self: _('New'))
    #name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    photo_patient = fields.Binary(string='Photo')
    #name = fields.Char(string='Nom', required=True)
    name = fields.Many2one('res.partner', string='Nom du partenaire', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    state = fields.Selection( [
        ('nouveau_client', 'Nouveau client'),
        ('prescriptionV', 'Prescription validée'),
        ('patient_en_traitement', 'Patient en cours de traitement'),
        ('patient_terminé', 'Patient ayant terminé')
    ], string='Statut du patient', default='nouveau_client', readonly=True, copy=False, index=True,
    track_visibility='onchange')
    titre = fields.Selection([
         ('M.', 'Monsieur'), ('Mme', 'Madame'),
         ('Mlle', 'Mademoiselle'), ('Vve', 'Veuve'),
    ], string='Titre', required=True)
    genre = fields.Selection( [
        ('H', 'Homme'), ('F', 'Femme')
    ], string='Genre', required=True)
    date_naissance = fields.Date(string='Date de naissance', required=True)
    age = fields.Char(string='Age', compute='compute_age')
    #nationalite = fields.Many2one('res.country', string='Nationalité', required=True)
    date = fields.Datetime(string='Date Requested', default=lambda s: fields.Datetime.now(), invisible=True)
    
    adresse_rue = fields.Char(string='Rue', size=128)
    adresse_ville = fields.Char(String='Ville', size=128, required=True)
    adresse_pays = fields.Many2one('res.country', string='Pays', ondelete='restrict')
    adresse_postal = fields.Char(string='Code postal')
    telephone = fields.Char(string='Téléphone', required=True)
    email = fields.Char(string='Email', required=True)
    note = fields.Text(string='Diagnostic')
    company_name = fields.Char('Company Name')
    note_kine = fields.Char()
    note_docteur = fields.Text()
    societe_patient = fields.Many2one('res.partner', string='Société', index=True)
    
    type_societe = fields.Selection([
        ('ipm', 'IPM'), ('assurance', 'Assurance')
    ], string='Type de la société')

    #Widget du patient
    total_invoiced = fields.Monetary(compute='_invoice_total', string="Total facturé")
    currency_id = fields.Many2one('res.currency', compute='_get_company_currency', readonly=True,
        string="Currency", help='Utility field to express amount currency')
    meeting_ids = fields.Many2many('calendar.event', 'calendar_event_res_partner_rel',
                                   'res_partner_id', 'calendar_event_id', string='Meetings', copy=False)
    meeting_count = fields.Integer(
        "# Meetings", compute='_compute_meeting_count')
    active = fields.Boolean(default=True)
    #Fin Widget du patient

    #suivi_traitement = fields.One2many('cmk.patient.suivitraitement', 'test_rod')
    #suivi_traitement = fields.Many2one('cmk.traitement', string='Nom traitement')
    suivi_traitement = fields.One2many('cmk.traitement', 'patient_traitement')

    #Aziz
    pathologie = fields.Many2many('cmk.pathologie', string='Pathologies')

    #Lamine
    kine_assigne = fields.Many2one('hr.employee', string='Kiné traitant')
    
#    etape = fields.Selection([
 #       ('nouveau', 'Nouveau'), ('validation_p', 'Validation prescription'),
  #      ('en cours', 'En cours de traitement'),
   #     ('termine', 'Terminé')], string='Etape_patient',
    #    copy=False, default='draft', index=True, readonly=True,
     #   help="* New: When the stock move is created and not yet confirmed.\n"
      #       "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"
       #      "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to be manufactured...\n"
        #     "* Available: When products are reserved, it is set to \'Available\'.\n"
         #    "* Done: When the shipment is processed, the state is \'Done\'.")

    #api pour créer de manière automatique le code patient : "PATXXX"
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('cmk.patient')
        vals['id_patient'] = sequence or '/'
        return super(CmkPatient, self).create(vals)

    #api pour calculer l'age à partir de la date de naissance et de la date actuelle
    @api.multi
    def compute_age(self):
        for data in self:
            if data.date_naissance:
                date_naissance = fields.Datetime.from_string(data.date_naissance)
                date = fields.Datetime.from_string(data.date)
                delta = relativedelta(date, date_naissance)
            data.age = str(delta.years) + ' ans'

    #api pour le formatage de l'adresse en un groupe : adresse_rue, adresse_ville, adresse_pays, adresse_postal
    @api.model
    def _get_default_address_formatage(self):
        return "%(adresse_rue)s\n%(adresse_ville)s\n%(adresse_pays)s %(adresse_postal)s"
            #<!--\n%(country_name)s-->

    # api pour le nombre de rdv
    @api.multi
    def _compute_meeting_count(self):
        for partner in self:
            partner.meeting_count = len(partner.meeting_ids)

    # api2 pour le calendrier
    @api.multi
    def schedule_meeting(self):
        partner_ids = self.ids
        partner_ids.append(self.env.user.partner_id.id)
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        action['context'] = {
            'search_default_partner_ids': self._context['partner_name'],
            'default_partner_ids': partner_ids,
        }
        return action

    #APIs pour la facturation
    @api.multi
    def _invoice_total(self):
        account_invoice_report = self.env['account.invoice.report']
        if not self.ids:
            self.total_invoiced = 0.0
            return True

    @api.multi
    def action_view_partner_invoices(self):
        self.ensure_one()
        action = self.env.ref('account.action_invoice_refund_out_tree').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('partner_id', 'child_of', self.id))
        return action

    #Fonctions du status bar
    @api.multi
    def valide_prescription_progressbar(self):
        return self.write({'state': 'prescriptionV'})

    @api.multi
    def traitement_en_cours_progressbar(self):
        return self.write({'state': 'patient_en_traitement'})

    @api.multi
    def termine_progressbar(self):
        return self.write({'state': 'patient_terminé'})
    #Fonctions du status bar