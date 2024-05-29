# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import datetime



class LogistiqueProduit(models.Model):
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _name = 'logistique.produit'
    _description = 'info.produit'

    reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                               default=lambda self: _('Nouveau'))
    active = fields.Boolean(string="Active", default=True, tracking=True)
    color = fields.Integer()

    logisticien = fields.Many2one('logistique.logisticien', string='Logisticien', tracking=True)
    transporteur = fields.Many2one('logistique.transporteur', string='Transporteur', tracking=True)
    sender = fields.Many2one('logistique.client', string='Client', copy=False, tracking=True, ondelete='restrict')
    name = fields.Char(string='Nom', tracking=True)
    surname = fields.Char(string='Prénom', tracking=True)
    mail = fields.Char(string='Mail', tracking=True)
    telephone = fields.Char('Téléphone', tracking=True)

    date = fields.Date(string='Date du devis', tracking=True, readonly=True, required=True, index=True, default=datetime.today())
    moyen_paiement = fields.Selection([('espece', 'Espece'), ('bank', 'Virement bancaire'),
                                          ('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')], default='cmr',
                                         string='Moyen de paiement', tracking=True)
    livraison_ok = fields.Selection([('oui', 'Oui'), ('non', 'Non')], "Livraison", tracking=True, default="non")
    frais_livraison = fields.Monetary('Frais Livraison', default=0)
    date_livraison = fields.Date('Date Livraison')
    adresse_livraison = fields.Char('Adresse Livraison')

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')
    state = fields.Selection([('devis', 'Mettre en devis'), ('annuler', 'Annuler'), ('devisenv', 'Envoyer pars mail'), ('bon', 'Bon de Commande'), ('payer', 'Payer Content')],
                           default="devis", string='States')
    active = fields.Boolean(string="Active", default=True, tracking=True)
    marchandiseline_ids = fields.One2many('logistique.marchacommande', 'commande_id', string="Article")
    frais_total = fields.Monetary(string='Frais Total', readonly=True, tracking=True, default=0, compute="_compute_price_total", store=True)

    # attribue des articles
    # marchandise_id = fields.Char(string='Marchandise', required=True, tracking=True)
    # name = fields.Char(string='Nom', required=True, tracking=True)
    # description = fields.Text(string='Description', tracking=True)
    # type = fields.Selection([('service', 'Produit_fini'), ('consumable', 'Produit_non_fini')], "Type d'article",
    #                         default='service', tracking=True)
    # barcode = fields.Char(string='Barcode', tracking=True)
    # quantity = fields.Integer(string='Quantite en stock', tracking=True, default='1', readonly=True)
    # quantity_ok = fields.Integer(string='Quantite', tracking=True, default='1')
    # sale_price = fields.Monetary(string='Prix de vente', required=True, tracking=True)
    # vente = fields.Monetary(string='Prix', readonly=True, tracking=True, compute='_sale_calculate')


    quantity_sold = fields.Integer(compute="compute_vendu")
    condition = fields.Text(string='Condition')
    total_count = fields.Float(compute='count_total')
    livraison = fields.Char(string="Livraison", tracking=True)
    frais_totals = fields.Monetary()
    # sum_total = fields.Monetary(string='Total', compute="_compute_sum_total")
    total_commande = fields.Monetary(string='Total commande',  compute="_compute_commande_total", store=True)

    # @api.depends('frais_total')
    # def _compute_sum_total(self):
    #     for record in self:
    #         record.sum_total += record.frais_total

    # function compute field d'un one2many
    @api.depends('marchandiseline_ids.vente')
    def _compute_commande_total(self):
        frais_totals = 0.0
        for record in self:
            for line in record.marchandiseline_ids:
                frais_totals += line.vente
            record.total_commande = frais_totals

    # @api.depends('total_commande', 'frais_livraison')
    # def _compute_price_total(self):
    #     for r in self:
    #         if not r.frais_livraison:
    #             r.frais_total = 0.0
    #         else:
    #             r.frais_total = r.total_commande + r.frais_livraison

    @api.depends('total_commande', 'frais_livraison')
    def _compute_price_total(self):
        for r in self:
            if r.livraison_ok == 'non':
                r.frais_total = r.total_commande
            else:
                r.frais_total = r.total_commande + r.frais_livraison
        

    def compte_total(self):
        return ()

    def action_livraison_move(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Livraison',
            'view_mode': 'tree',
            'res_model': 'logistique.delivery',
            'domain': [('delivery_id', 'in', self.reference)],
            'context': {'create': False}
        }


    @api.model
    def create(self, vals):
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.produit') or _('Nouveau')
        res = super(LogistiqueProduit, self).create(vals)
        return res

    @api.depends('frais_total')
    def count_total(self):
        for record in self:
            record.total_count = record.frais_total

    # @api.constrains('date_livraison')
    # def _check_date_end(self):
    #     for record in self:
    #         if record.date_livraison <= fields.Date.today():
    #             raise ValidationError("La date ne peut pas etre dans le passe ou etre aujourd'hui")


    def action_devis(self):
        for rec in self:
            rec.state = 'devis'

    def action_payer(self):
        for rec in self:
            rec.state = 'payer'

    def action_annuler(self):
        for rec in self:
            rec.state = 'annuler'

    def action_devisenv(self):
        for rec in self:
            rec.state = 'devisenv'

    # function pour decrementer et incrementer relier a une action
    def action_bon(self):
        for rec in self:
            rec.state = 'bon'
            rec.marchandiseline_ids.increment_marchandise()
            rec.marchandiseline_ids.decrement_stock_marchandise()
            rec.marchandiseline_ids._check_quantité()
            rec.marchandiseline_ids._check_quantité_ok()


    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = '[' + rec.reference + ']'
    #         result.append((rec.id, name))
    #     return result

#same fonction but 1st convert reference into name
    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, field.reference))
        return res

    @api.onchange("sender")
    def _onchange_sender(self):

        if not self.sender:
            self.update(
                {
                    "name": False,
                    "surname": False,
                    "telephone": False,
                    "mail": False,
                }
            )
        else:
            self.update(
                {
                    "name": self.sender.name,
                    "surname": self.sender.surname,
                    "telephone": self.sender.telephone,
                    "mail": self.sender.mail,
                }
            )


 # contraintes pour les livraison
 #    @api.constrains('date_livraison', 'date')
 #    def _check_date(self):
 #        for record in self:
 #            if record.date_livraison <= record.date:
 #                raise ValidationError("Nous ne pouvons pas vous livrer le meme jour. Veillez changer la date de livraison")


# Nouvelle class
class LogistiqueCommandeLine(models.Model):
    _name = 'logistique.commandeline'
    _description = 'commande_line infos'

    commande_id = fields.Many2one('logistique.produit', string="Commande")
    livraison_id = fields.Many2one('logistique.livraison', string="Livraison")
    delivery_id = fields.Many2one('logistique.delivery', string="Delivery")
    date = fields.Date(string='Date du devis', tracking=True)
    date_livraison = fields.Date('Date Livraison')
    moyen_paiement = fields.Selection([('espece', 'Espece'), ('bank', 'Virement bancaire'),('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')], default='cmr',string='Moyen de paiement', tracking=True)
    logisticien = fields.Many2one('logistique.logisticien', string='Logisticien', tracking=True)
    sender = fields.Many2one('logistique.client', string='Client', copy=False, tracking=True, ondelete='restrict')
    frais_livraison = fields.Monetary('Frais Livraison', default=0)
    name = fields.Char(string='Nom', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    quantity_ok = fields.Integer(string='Quantite', tracking=True, default='1')
    sale_price = fields.Monetary(string='Prix de vente', required=True, tracking=True)
    vente = fields.Monetary(string='Prix', readonly=True, tracking=True)
    frais_total = fields.Monetary(string='Frais Total', readonly=True, tracking=True, default=0)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')

    # contraintes pour les livraison
    @api.constrains('date_livraison', 'date')
    def _check_date(self):
        for record in self:
            if record.date_livraison <= record.date:
                raise ValidationError(
                    "Nous ne pouvons pas vous livrer le meme jour. Veillez changer la date de livraison")

    @api.onchange('commande_id')
    def _onchange_commande_id(self):
        if not self.commande_id:
            self.update(
                {
                    'moyen_paiement': False,
                    'date': False,
                    'date_livraison': False,
                    'logisticien': False,
                    'sender': False,
                    'frais_livraison': False,
                    'name': False,
                    'description': False,
                    'quantity_ok': False,
                    'sale_price': False,
                    'vente': False,
                    'frais_total': False,

                }
            )
        else:
            self.update(
                {
                    "moyen_paiement": self.commande_id.moyen_paiement,
                    "date": self.commande_id.date,
                    "date_livraison": self.commande_id.date_livraison,
                    "logisticien": self.commande_id.logisticien.name,
                    "sender": self.commande_id.sender.name,
                    "frais_livraison": self.commande_id.frais_livraison,
                    "name": self.commande_id.marchandiseline_ids.name,
                    "description": self.commande_id.marchandiseline_ids.description,
                    "quantity_ok": self.commande_id.marchandiseline_ids.quantity_ok,
                    "sale_price": self.commande_id.marchandiseline_ids.sale_price,
                    "vente": self.commande_id.marchandiseline_ids.vente,
                    "frais_total": self.commande_id.frais_total,
                }
            )