# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class LogistiqueLivraison(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _name = 'logistique.livraison'
   _description = 'info. livraison'

   reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                           default=lambda self: _('Nouveau'))
   # user_id = fields.Many2one('res.users', 'Users', required=True, index=True, ondelete='cascade')
   # marchandise_id = fields.One2many('logistique.marchandise', 'id_article', string='Article')
   sender = fields.Many2one('logistique.client', string='Client', tracking=True, required=True)
   logisticien = fields.Many2one('logistique.logisticien', string='Responsable Logisticien', tracking=True)
   transporteur = fields.Many2one('logistique.transporteur', string='Transporteur', tracking=True,
                                 required=True)
   mail = fields.Char(string='Mail client', tracking=True)
   commande_id = fields.Many2one('logistique.produit', string='Commande Id', tracking=True)
   commandline_ids = fields.One2many('logistique.commandeline', 'livraison_id', string="Livraison")
   envoyeur = fields.Char(string='Entrepot Envoyeur', tracking=True,)
   destination = fields.Char(string='Destination Commande', tracking=True)
   currency_id = fields.Many2one('res.currency',
                                 default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                 readonly=True, required=True, string='Currency')
   frais_livraison= fields.Monetary(string='Frais de livraison', tracking=True)
   date_livraison = fields.Date(string="Date de livraison prévue", tracking=True)
   total = fields.Monetary(string='Total', compute="_calculate_livraison")
   name = fields.Char(string='Nom', tracking=True)
   description = fields.Text(string='Description', tracking=True)
   quantity = fields.Integer(string='Quantite en stock', tracking=True)
   sale_price = fields.Monetary(string='Prix de vente', tracking=True)
   date = fields.Datetime(string='Date du devis', tracking=True)
   moyen_paiement = fields.Selection([('espece', 'Espece'), ('bank', 'Virement bancaire'),
                                      ('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')], default='cmr',
                                     string='Moyen de paiement', tracking=True)
   state = fields.Selection([('en_cours', 'En cours'), ('valider', 'Valider'),
                             ('payer', 'Payer'), ('annuler', 'Annuler'), ('send', 'Envoyer par mail')], default='en_cours',
                            string='Status', tracking=True)
   active = fields.Boolean(string="Active", default=True, tracking=True)
   total_count = fields.Integer(compute='count_total')
   operation = fields.Char()

   def action_operartion_move(self):
       return ()

   def compte_total(self):
       return ()

   @api.depends('frais_livraison')
   def count_total(self):
       for record in self:
           record.total_count += record.frais_livraison


   @api.depends('frais_livraison')
   def _calculate_livraison(self):
       for r in self:
           if not r.frais_livraison:
               r.total = 0.0
           else:
               r.total = r.frais_livraison

   @api.model
   def create(self, vals):
       if vals.get('reference', _('Nouveau')) == _('Nouveau'):
           vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.livraison') or _('Nouveau')
       res = super(LogistiqueLivraison, self).create(vals)
       return res


   def action_en_cours(self):
       self.state = 'en_cours'

   def action_valider(self):
       self.state = 'valider'
       return {
           'effect': {
               'fadeout': 'show',
               'message': 'livraison valider',
               'type': 'rainbow_man',
           }
       }

   def action_payer(self):
       self.state = 'payer'

   def action_annuler(self):
       self.state = 'annuler'

   def action_send(self):
       self.state = 'send'
       # template_id = self.env.ref('cs_shipping.email_template_livraison').id
       # template = self.env['mail.template'].browse(template_id)
       # template.send_mail(self.id, force_send=True)

   def name_get(self):
       result = []
       for rec in self:
           name = '[' + rec.reference + ']'
           result.append((rec.id, name))
       return result