# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime


class LogistiqueFree(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'logistique.free'
    _description = 'info.free'

    name = fields.Char(string='Nom', required=True, tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    mail = fields.Char(string='Email', tracking=True)
    note = fields.Text(string='Note', tracking=True)



class LogistiqueBlog(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'logistique.blog'
    _description = 'info.blog'

    date = fields.Date(string='Date', tracking=True)
    image = fields.Binary(string='Image', tracking=True)
    description = fields.Text(string='Description', tracking=True)
    title = fields.Char(string='Title', tracking=True)

