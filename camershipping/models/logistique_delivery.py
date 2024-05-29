# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class LogistiqueDelivery(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _name = 'logistique.delivery'
   _description = 'info. delivery'

   commandline_ids = fields.One2many('logistique.commandeline', 'delivery_id', string="Delivery")
   reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                           default=lambda self: _('Nouveau'))

   delivery_id = fields.Many2one('logistique.delivery', string="Delivery")
   date = fields.Date(string='Date du devis', tracking=True)
   date_livraison = fields.Date('Date Livraison')
   moyen_paiement = fields.Selection(
      [('espece', 'Espece'), ('bank', 'Virement bancaire'), ('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')],
      default='cmr', string='Moyen de paiement', tracking=True)
   logisticien = fields.Many2one('logistique.logisticien', string='Logisticien', tracking=True)
   sender = fields.Many2one('logistique.client', string='Client', copy=False, tracking=True, ondelete='restrict')
   frais_livraison = fields.Monetary('Frais Livraison', default=0)
   name = fields.Char(string='Nom', required=True, tracking=True)
   description = fields.Text(string='Description', tracking=True)
   quantity_ok = fields.Integer(string='Quantite', tracking=True, default='1')
   sale_price = fields.Monetary(string='Prix de vente', required=True, tracking=True)
   vente = fields.Monetary(string='Prix', readonly=True, tracking=True)
   frais_total = fields.Monetary(string='Frais Total', readonly=True, tracking=True, default=0)
   currency_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')

   # same fonction but 1st convert reference into name
   def name_get(self):
      res = []
      for field in self:
         res.append((field.id, field.reference))
      return res

   @api.model
   def create(self, vals):
      if vals.get('reference', _('Nouveau')) == _('Nouveau'):
         vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.delivery') or _('Nouveau')
      res = super(LogistiqueDelivery, self).create(vals)
      return res



