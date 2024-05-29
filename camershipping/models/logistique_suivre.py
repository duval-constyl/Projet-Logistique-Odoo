# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class LogistiqueSuivre(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _name = 'logistique.suivre'
   _description = 'info. pour suivre'

   type = fields.Selection([('expedition', 'Expedition'), ('livraison', 'Livraison')], "Type d'envoie",
                            required=True, tracking=True)
   ville = fields.Char(string='Ville de reception', tracking=True)
   position = fields.Text(string='Position', tracking=True)
   date = fields.Datetime(string='Date de reception', required=True, tracking=True)
   reference_liv =fields.Many2one('logistique.livraison', 'Reference Livraison', tracking=True)
   reference_exp = fields.Many2one('logistique.expedition', 'Reference Expedition', tracking=True)
