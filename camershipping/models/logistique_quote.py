# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class LogistiqueQuote(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _name = 'logistique.quote'
   _description = "quote sur l'expedition"

   type_coliss = fields.Char(string='Article Type', tracking=True)
   transport_meanss = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                       ('terrestre', 'Road Transport'), ('rail', 'Rail Transport')],default='terrestre', string='Transport Means', tracking=True, )
   qtys = fields.Integer(string='Quantity', tracking=True, default=1)
   prixs = fields.Char(string='Price per Kilo', tracking=True, default='1000 FCFA')
   sub_totals = fields.Monetary(string='Sub_total', tracking=True, compute='_calculates_subtotal')
   masss = fields.Integer(string='Mass', tracking=True)
   volumes = fields.Integer(string='Volume', tracking=True)
   heights = fields.Integer(string='Height', tracking=True)
   poidss = fields.Float(string='Weight', tracking=True, compute='_poids_article')
   currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')
   totals = fields.Monetary(string="Total", compute='_totals_calculates')
   state = fields.Selection([('none', 'None verified'), ('modifier', 'Modified'),
                             ('valide', 'Valide'), ('envoyer', 'Send')], default='none',
                            string='Status', tracking=True)



   @api.depends('masss')
   def _poids_article(self):
       for r in self:
           if not r.masss:
               r.poidss = 0.0
           else:
               r.poidss = r.masss * 9.81

   @api.depends('poidss')
   def _calculates_subtotal(self):
       for r in self:
           if not r.poidss:
               r.sub_totals = 0.0
           else:
               r.sub_totals = r.poidss * 1000

   @api.depends('sub_totals', 'qtys')
   def _totals_calculates(self):
       for r in self:
           if not r.qtys:
               r.totals = 0.0
           else:
               r.totals = r.qtys * r.sub_totals

   @api.model
   def action_none(self):
    self.state = 'none'

   def action_valide(self):
    self.state = 'valide'
    return {
         'effect': {
              'fadeout': 'show',
              'message': 'Pré-expedition valider',
              'type': 'rainbow_man',
        }
    }

   def action_modifier(self):
    self.state = 'modifier'

   def action_envoyer(self):
    self.state = 'envoyer'
    # template_id = self.env.ref('cs_shipping.email_template_expedition').id
    # template = self.env['mail.template'].browse(template_id)
    # template.send_mail(self.id, force_send=True)




