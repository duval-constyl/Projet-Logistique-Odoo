# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class LogistiqueSubscribe(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'logistique.subscribe'

    name = fields.Char(string='Nom', required=True, tracking=True)
    mail = fields.Char(string='Email', tracking=True)
