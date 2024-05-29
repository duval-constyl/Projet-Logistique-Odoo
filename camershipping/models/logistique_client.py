# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class LogistiqueClient(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'logistique.client'
    _description = 'info.client'


    reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                            default=lambda self: _('Nouveau'))
    color = fields.Integer()

    name = fields.Char(string='Nom', required=True, tracking=True)
    surname = fields.Char(string='Prenom', tracking=True)
    mail = fields.Char(string='Mail', tracking=True)
    country = fields.Many2one('res.country', string='Nationalité', ondelete='restrict', tracking=True)
    telephone = fields.Char('Telephone', tracking=True)
    adresse = fields.Char(string='Adresse', tracking=True)
    produit_id = fields.One2many('logistique.produit','sender', string="Produit")
    expedition_id = fields.One2many('logistique.expedition', 'sender', string="Expedition")

    #encrypt password
    password = fields.Char(string='Mot de Passe', tracking=True)
    confirm_password = fields.Char(string='Confirmation MDP', tracking=True)

    # incrementation sequencial d'identifiant client
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.client') or _('Nouveau')
        res = super(LogistiqueClient, self).create(vals)
        return res

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, field.reference))
        return res

    # contrainte mail
    _sql_constraints = [
        ('email_uniq', 'UNIQUE (mail)', 'adresse mail deja utiliser')
    ]