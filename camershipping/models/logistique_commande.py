# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class LogistiqueCommande(models.Model):
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _name = 'logistique.commande'
    _description = 'info.commande'

    reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                               default=lambda self: _('Nouveau'))
    transporteur = fields.Many2one('logistique.transporteur', string='Transporteur', tracking=True)
    logisticien = fields.Many2one('logistique.logisticien', string='Logisticien', tracking=True)
    sender = fields.Many2one('logistique.client', string='Client', tracking=True)
    date = fields.Datetime(string='Date du devis', tracking=True)
    moyen_paiement = fields.Selection([('espece', 'Espece'), ('bank', 'Virement bancaire'),
                                          ('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')], default='cmr',
                                         string='Moyen de paiement', tracking=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')
    date_livraison = fields.Date(string='Date de Livraison', tracking=True)
    destination = fields.Char(string='Destination',tracking=True )
    state = fields.Selection([('devis', 'Devis'), ('annuler', 'Annuler'), ('devisenv', 'Devis Envoyer'), ('bon', 'Bon de Commande')],
                           default="devis", string='States')
    active = fields.Boolean(string="Active", default=True, tracking=True)
    livraison = fields.Boolean(string="Livraison",tracking=True)
    marchandiseline_ids = fields.One2many('logistique.marchacommande', 'commande_id', string="Article")
    frais_total = fields.Monetary(string='Frais total', readonly=True, tracking=True, default=0)

    # attribue des articles
    marchandise_id = fields.Char(string='Marchandise', required=True, tracking=True)
    name = fields.Char(string='Nom', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    type = fields.Selection([('service', 'Produit_fini'), ('consumable', 'Produit_non_fini')], "Type d'article",
                            default='service', tracking=True)
    barcode = fields.Char(string='Barcode', tracking=True)
    quantity = fields.Integer(string='Quantite', tracking=True, default='1')
    sale_price = fields.Monetary(string='Prix de vente', required=True, tracking=True)
    # tax = fields.Many2one('account.tax', string='Taxes', context={'active_test': False})
    vente = fields.Monetary(string='Prix', readonly=True, tracking=True, compute='_sale_calculate')
    total = fields.Monetary(string='Total', readonly=True, tracking=True, compute='_total_calculate')


    @api.model
    def create(self, vals):
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.commande') or _('Nouveau')
        res = super(LogistiqueCommande, self).create(vals)
        return res


    def action_devis(self):
        self.state = 'devis'

    def action_annuler(self):
        self.state = 'annuler'

    def action_devisenv(self):
        self.state = 'devisenv'

    def action_bon(self):
        self.state = 'bon'

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + ']'
            result.append((rec.id, name))
        return result



class LogistiqueCommandeLine(models.Model):
    _name = 'logistique.commandeline'
    _description = 'commande_line infos'

    commande_id = fields.Many2one('logistique.commande', string="Commande")
    livraison_id = fields.Many2one('logistique.livraison', string="Livraison")
    date = fields.Datetime(string='Date du devis', tracking=True)
    moyen_paiement = fields.Selection([('espece', 'Espece'), ('bank', 'Virement bancaire'),
                                       ('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')], default='cmr',
                                      string='Moyen de paiement', tracking=True)

    @api.onchange('commande_id')
    def _onchange_commande_id(self):
        if not self.commande_id:
            self.update(
                {
                    'moyen_paiement': False,
                    'date': False,
                }
            )
        else:
            self.update(
                {
                    "moyen_paiement": self.commande_id.moyen_paiement,
                    "date": self.commande_id.date,

                }
            )