# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class LoginExpedition(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _inherit = 'logistique.quote'



class Expedition(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _inherit = 'logistique.expedition'


class Commexpe(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _inherit = 'logistique.commexpe'