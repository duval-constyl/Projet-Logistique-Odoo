# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class LogistiqueContainer(models.Model):
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _name = 'logistique.container'
    _description = 'info.container'

    reference = fields.Char(string='Reference', readonly=True, required=True, copy=False,
                               default=lambda self: _('Nouveau'))
    container = fields.Char(string='Numero de Conteneur', required=True, tracking=True)
    expedition_id = fields.Many2one('logistique.expedition', string="Expeditions")
    expedition_ids = fields.One2many('logistique.conteneurline', 'conteneur_id', string='Expedition')
    state = fields.Selection([('draft', 'Draft'), ('cancel', 'Cancel'), ('done', 'Done'), ('send', 'Send')],
                             default="draft", string='States')
    name = fields.Char(string='Destinateur')
    envoyer = fields.Char(string='Entrepot Envoyeur', tracking=True)
    destination = fields.Char(string='Entrepot Destiné', tracking=True)
    sender = fields.Char(string='Client', tracking=True)
    moyen_transport = fields.Char(string="Moyen d'expedition", tracking=True)
    qty = fields.Integer(string='Quantité', tracking=True)
    logisticien = fields.Char(string='Responsable cs_shipping', tracking=True)
    type_colis = fields.Char(string='Type de colis', tracking=True)
    prix = fields.Monetary(string='Prix Unitaire', tracking=True)
    total = fields.Monetary(string='Total', tracking=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')
    operation = fields.Char()

    def action_operartion_move(self):
        return ()

    @api.model
    def create(self, vals):
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.container') or _('Nouveau')
        res = super(LogistiqueContainer, self).create(vals)
        return res

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, field.reference))
        return res

    def action_done(self):
        self.state = 'done'

    def action_send(self):
        self.state = 'send'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

