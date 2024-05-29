# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class LoginExpedition(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _inherit = 'logistique.client'