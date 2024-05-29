# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class LogistiqueLogisticien(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'logistique.logisticien'
    _description = 'info.logisticien'
    _log_access = False

    reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                            default=lambda self: _('Nouveau'))
    surname = fields.Char(string='Prenom', tracking=True)
    name = fields.Char(string='Nom', required=True, tracking=True)
    mail = fields.Char(string='Mail', tracking=True)
    nationality = fields.Many2one('res.country', string='Nationalité', ondelete='restrict', tracking=True)
    password = fields.Char(string='Mot de Passe', tracking=True)
    confirm_password = fields.Char(string='Confirmation MDP', tracking=True)
    telephone = fields.Char('Telephone', tracking=True)
    adresse = fields.Char(string='Adresse', tracking=True)
    ufile = fields.Binary(tracking=True)
    state = fields.Selection([('fonction', 'En Fonction'), ('annuler', 'Annuler'), ('repos', 'En Repos')],
                             default="repos", string='States')

    # incrementation sequencial d'identifiant logisticien
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.logisticien') or _('Nouveau')
        res = super(LogistiqueLogisticien, self).create(vals)
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