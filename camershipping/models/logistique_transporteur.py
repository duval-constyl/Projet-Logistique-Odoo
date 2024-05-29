# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class LogistiqueTransporteur(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'logistique.transporteur'
    _description = 'info.transporteur'
    _log_access = False

    reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                            default=lambda self: _('Nouveau'))
    name = fields.Char(string='Nom', required=True, tracking=True)
    surname = fields.Char(string='Prenom', tracking=True)
    mail = fields.Char(string='Mail', tracking=True)
    password = fields.Char(string='Mot de Passe', tracking=True)
    confirm_password = fields.Char(string='Confirmation MDP', tracking=True)
    telephone = fields.Char('Telephone', tracking=True)
    adresse = fields.Char(string='Adresse', tracking=True)
    nationality = fields.Many2one('res.country', string='Nationalité', ondelete='restrict', tracking=True)
    user = fields.Selection([('transporteur', 'Transporteur')], 'Utilisateur', default="transporteur", required=True,
                            tracking=True)
    ufile = fields.Binary(tracking=True)
    permis = fields.Selection([('permis1', 'Permis A1'), ('permis2', 'Permis A'), ('permis3', 'Permis B'),
                               ('permis4', 'Permis BE'), ('permis5', 'Permis C'), ('permis6', 'Permis CE'),
                               ('permis7', 'Permis D'), ('permis8', 'Permis DE'), ('permis9', 'Permis FA1'),
                               ('permis10', 'Permis FA'), ('permis11', 'Permis FB'), ('permis12', 'Permis G')],
                              default="permis3",
                              string='Type de Permis', tracking=True)
    vehicule = fields.Char(string='Véhicule Attribué', tracking=True)
    num_vehicule = fields.Char(string='Numero Véhicule', tracking=True)
    trajet = fields.Char(string='Trajet Transporteur', tracking=True)
    state = fields.Selection([('fonction', 'En Fonction'), ('annuler', 'Annuler'), ('repos', 'En Repos')],
                             default="repos", string='States')

    # incrementation sequencial d'identifiant logisticien
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.transporteur') or _('Nouveau')
        res = super(LogistiqueTransporteur, self).create(vals)
        return res

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, field.name))
        return res

    def action_fonction(self):
        self.state = 'fonction'

    def action_repos(self):
        self.state = 'repos'

    def action_annuler(self):
        self.state = 'annuler'

    # contrainte mail
    _sql_constraints = [
        ('email_uniq', 'UNIQUE (mail)', 'adresse mail deja utiliser')
    ]