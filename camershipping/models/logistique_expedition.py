# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class LogistiqueExpedition(models.Model):
   _inherit = ["mail.thread", 'mail.activity.mixin']
   _name = 'logistique.expedition'
   _description = 'info. expeditions'



   reference = fields.Char(string='Tracking_Code', readonly=True,  copy=False,
                           default=lambda self: _('Nouveau'))
   color = fields.Integer()

   # user_id = fields.Many2one('res.users', 'Users', required=True, index=True, ondelete='cascade')
   sender = fields.Many2one('logistique.client', string='Client', tracking=True)
   name = fields.Char(string='Nom', tracking=True)
   telephone = fields.Char('Téléphone', tracking=True)
   expedition_ids = fields.One2many('logistique.commexpe', 'expedition_id', string='Commande')
   logisticien = fields.Many2one('logistique.logisticien', string='Responsable cs_shipping', tracking=True)
   # user_id = fields.Many2one('res.users', 'Users', required=True, index=True, ondelete='cascade')
   moyen_transport = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                       ('terrestre', 'Road Transport'),('rail', 'Rail Transport')], default='terrestre',
                                      string='Moyen d\'expedition', tracking=True,)
   moyen_paiement = fields.Selection([('espece', 'Espece'), ('bank', 'Virement bancaire'),
                                      ('cheque', 'Cheque'), ('cmr', 'Orange/MTN Money')], default='cmr',
                                     string='Moyen de paiement', tracking=True)
   currency_id = fields.Many2one('res.currency',
                                 default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                 readonly=True,  string='Currency')
   frais_total = fields.Monetary(string="Frais D'envoie", tracking=True)
   envoyer = fields.Char(string='Entrepot Envoyeur', tracking=True,  )
   destination = fields.Char(string='Entrepot Destiné', tracking=True, )
   qty = fields.Integer(string='Quantité', tracking=True)
   prix = fields.Monetary(string="Prix unitaire",  tracking=True)
   heure_depart = fields.Datetime(string='Date/Heure de départ', copy=False, tracking=True)
   heure_pickup = fields.Date(string='Date/Heure de ramassage_colis',  copy=False, tracking=True)
   date_livraison = fields.Date(string="Date d'expédition ", tracking=True)
   state = fields.Selection([('en_cours', 'En cours'), ('valider', 'Valider'),
                             ('payer', 'Payer'), ('annuler', 'Annuler'), ('send', 'Envoyer par mail'),('telephone', 'Ecrire au Destinateur')], default='en_cours',
                            string='Status', tracking=True)
   names = fields.Char(string='Nom')
   adresse = fields.Char("Adresse")
   nationality = fields.Many2one('res.country', string='Nationalité', ondelete='restrict', tracking=True)
   city = fields.Char(string='Cité')
   email = fields.Char(string='Mail')
   phone = fields.Char(string='Telephone')
   zip = fields.Char(string='Zip')
   card_id = fields.Char(string='Identifiant de carte national')
   active = fields.Boolean(string="Active", default=True, tracking=True)
   total = fields.Monetary(string="Total", compute='_total_expedition',
                           store=True, readonly=True, tracking=4, ondelete="cascade")
   total_otm = fields.Float()
   condition = fields.Char(string="Condition", tracking=True)
   type_colis = fields.Char(string='Type de Marchandise', tracking=True)
   transport_means = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                       ('terrestre', 'Road Transport'),('rail', 'Rail Transport')], default='terrestre',
                                      string='Transport Means', tracking=True,)
   qty = fields.Integer(string='Quantité', tracking=True)
   prix = fields.Monetary(string='Prix Unitaire', tracking=True)
   sub_total = fields.Monetary(string='Sub_total', tracking=True)
   prix_commande = fields.Monetary(string='Total commande', tracking=True, compute='_total_calculates')
   mass = fields.Integer(string='Mass', tracking=True)
   volume = fields.Integer(string='Volume', tracking=True)
   poids = fields.Float(string='Poids', tracking=True)
   height = fields.Float(string='Height', tracking=True)
   currency_id = fields.Many2one('res.currency',
                                 default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                 readonly=True, string='Currency')
   operation = fields.Char()
   total_count = fields.Integer(compute='count_total')
   expedition = fields.Char(string="Expedition", tracking=True)
   date_enres = fields.Datetime(string='Date Enregistrement', tracking=True, readonly=True, required=True, index=True,
                          default=datetime.today())

   type_colis = fields.Char(string='Type de Marchandise', tracking=True)
   transport_means = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                       ('terrestre', 'Road Transport'), ('rail', 'Rail Transport')],
                                      default='terrestre',
                                      string='Transport Means', tracking=True, )
   qty = fields.Integer(string='Quantité', tracking=True, default=1)
   prix = fields.Char(string='Prix par Kilo', tracking=True, default='1000 FCFA')
   sub_total = fields.Monetary(string='Sub_total', tracking=True, compute='_calculate_subtotal')
   mass = fields.Integer(string='Mass', tracking=True)
   volume = fields.Integer(string='Volume', tracking=True)
   poids = fields.Float(string='Poids', tracking=True, compute='_poids_article')
   height = fields.Float(string='Height', tracking=True)

   #  #contrainte pour le jour present
   @api.constrains('date_livraison')
   def _check_date_livraison(self):
       for record in self:
           if record.date_livraison <= fields.Date.today():
               raise ValidationError("La date d'expedition ne peut pas etre egal à la date d'aujourd'hui")

   # function compute field d'un one2many
   @api.depends('expedition_ids.sub_total')
   def _total_calculates(self):
       total_otm = 0.0
       for record in self:
           for line in record.expedition_ids:
               total_otm += line.sub_total
           record.prix_commande = total_otm


       # contraintes pour les livraison
   @api.constrains('date_livraison', 'heure_pickup')
   def _check_date(self):
       for record in self:
           if record.heure_pickup >= record.date_livraison:
               raise ValidationError(
                   "Dans les normes la date de ramasage doit etre inférieur à la date d'expedition ")

   def action_operartion_move(self):
       return ()

   def action_expedition_move(self):
       return ()

   def compte_total(self):
       return ()

   @api.depends('frais_total')
   def count_total(self):
       for record in self:
           record.total_count += record.total

   @api.model
   def create(self, vals):
       # create returns the newly created record
       rec = super(LogistiqueExpedition, self).create(vals)
       print(rec.sub_total)
       # if you want to set the value just do this
       rec.total = rec.sub_total  # this will trigger write call to update the field in database
       return rec

   @api.depends('prix_commande', 'frais_total')
   def _total_expedition(self):
       for r in self:
           if not r.frais_total:
               r.total = 0.0
           else:
               r.total = r.frais_total + r.prix_commande


   @api.model
   def create(self, vals):
       if vals.get('reference', _('Nouveau')) == _('Nouveau'):
           vals['reference'] = self.env['ir.sequence'].next_by_code('logistique.expedition') or _('Nouveau')
       res = super(LogistiqueExpedition, self).create(vals)
       return res

   def name_get(self):
       res = []
       for field in self:
           res.append((field.id, field.reference))
       return res

   def action_en_cours(self):
       for rec in self:
        rec.state = 'en_cours'

   def action_telephone(self):
       for rec in self:
           if not rec.phone:
               raise ValidationError(_("Veuillez inserer un vrai numero whatsapp"))
           msg = 'Bonjour %s voici votre facture %s' % (rec.names, rec.reference)
           whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (rec.phone, msg)
       return {
           'type': 'ir.actions.act_url',
           'target': 'new',
           'url': whatsapp_api_url
       }

   def action_valider(self):
       for rec in self:
        rec.state = 'valider'
       return {
           'effect': {
               'fadeout': 'show',
               'message': 'expedition valider',
               'type': 'rainbow_man',
           }
       }

   def action_payer(self):
       for rec in self:
        rec.state = 'payer'

   def action_annuler(self):
       for rec in self:
         rec.state = 'annuler'

   def action_send(self):
       for rec in self:
        rec.state = 'send'
       # template_id = self.env.ref('camershipping.expedition_qweb')
       # self.message_post_with_template(template_id.id)
       # self.message_post_with_view('camershipping.expedition_qweb',values={'extra_data': 'test'})
       #
       # template_id = self.env.ref('camershipping.email_template_expedition').id
       # template = self.env['mail.template'].browse(template_id)
       # template.send_mail(self.id, force_send=True)

   def action_expedition_move(self):
       return{
           'name': _('Container'),
           'res_model': 'logistique.container',
           'view_mode': 'list,form',
           'context': {},
           'target': 'current',
           'type': 'ir.actions.act_window',
       }

   @api.onchange("sender")
   def _onchange_sender(self):
        if not self.sender:
            self.update(
                {
                    "name": False,
                    "telephone": False,
                }
            )
        else:
            self.update(
                {
                    "name": self.sender.name,
                    "telephone": self.sender.telephone,
                }
            )



class LogistiqueConteneur(models.Model):
    _name = 'logistique.conteneurline'

    expedition_id = fields.Many2one('logistique.expedition', string="Expedition")
    conteneur_id = fields.Many2one('logistique.container', string="Conteneur")
    envoyer = fields.Char(string='Entrepot Envoyeur', tracking=True)
    destination = fields.Char(string='Entrepot Destiné', tracking=True)
    sender = fields.Char(string='Client', tracking=True)
    moyen_transport = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                       ('terrestre', 'Road Transport'),('rail', 'Rail Transport')], default='terrestre',
                                      string='Moyen d\'expedition', tracking=True,)
    transport_means = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                        ('terrestre', 'Road Transport'), ('rail', 'Rail Transport')],
                                       default='terrestre',
                                       string='Transport Means', tracking=True, )
    logisticien = fields.Char(string='Responsable Logisticien', tracking=True)
    type_colis = fields.Char(string='Type de Marchandise', tracking=True)
    qty = fields.Integer(string='Quantité', tracking=True)
    sub_total = fields.Monetary(string='Prix Unitaire', tracking=True)
    poids = fields.Float(string='Poids', tracking=True)
    total = fields.Monetary(string='Total', tracking=True)
    height = fields.Float(string='Height', tracking=True)
    names = fields.Char(string='Destinateur')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')

    @api.onchange('expedition_id')
    def _onchange_expedition_id(self):
        if not self.expedition_id:
            self.update(
                {
                    'envoyer': False,
                    'destination': False,
                    'sender': False,
                    'moyen_transport': False,
                    'logisticien': False,
                    'type_colis': False,
                    'sub_total': False,
                    'qty': False,
                    'transport_means': False,
                    'total': False,
                    'poids': False,
                    'names': False,
                    'height': False,
                }
            )
        else:
            self.update(
                {
                    "envoyer": self.expedition_id.envoyer,
                    "destination": self.expedition_id.destination,
                    "sender": self.expedition_id.sender.name,
                    "moyen_transport": self.expedition_id.moyen_transport,
                    'logisticien': self.expedition_id.logisticien.name,
                    "type_colis": self.expedition_id.expedition_ids.type_colis,
                    "transport_means": self.expedition_id.expedition_ids.transport_means,
                    "qty": self.expedition_id.expedition_ids.qty,
                    "poids": self.expedition_id.expedition_ids.poids,
                    "sub_total": self.expedition_id.expedition_ids.sub_total,
                    "total": self.expedition_id.expedition_ids.total,
                    "names": self.expedition_id.names,
                    "height": self.expedition_id.expedition_ids.height,
                }
            )





class LogistiqueCommExpe(models.Model):
    _name = 'logistique.commexpe'

    expedition_id = fields.Many2one('logistique.expedition', string="Expedition")
    type_colis = fields.Char(string='Type de Marchandise', tracking=True)
    transport_means = fields.Selection([('maritime', 'Sea Transport'), ('fret', 'Air Transport'),
                                       ('terrestre', 'Road Transport'),('rail', 'Rail Transport')], default='terrestre',
                                      string='Transport Means', tracking=True,)
    qty = fields.Integer(string='Quantité', tracking=True, default=1)
    prix = fields.Char(string='Prix par Kilo', tracking=True, default='1000 FCFA')
    sub_total = fields.Monetary(string='Sub_total', tracking=True, compute='_calculate_subtotal')
    mass = fields.Integer(string='Mass', tracking=True)
    volume = fields.Integer(string='Volume', tracking=True)
    poids = fields.Float(string='Poids', tracking=True, compute='_poids_article')
    height = fields.Float(string='Height', tracking=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, string='Currency')
    total = fields.Monetary(string="Total", compute='_total_calculates',
                            store=True, readonly=True, tracking=4, ondelete="cascade")

    @api.depends('mass')
    def _poids_article(self):
        for r in self:
            if not r.mass:
                r.poids = 0.0
            else:
                r.poids = r.mass * 9.81

    @api.depends('poids', 'qty')
    def _calculate_subtotal(self):
        for r in self:
            if not r.poids:
                r.sub_total = 0.0
            else:
                r.sub_total = (r.poids * 3000) * r.qty

    @api.onchange('expedition_id')
    def _onchange_expedition_id(self):
        if not self.expedition_id:
            self.update(
                {
                    'type_colis': False,
                    'qty': False,
                    'prix': False,
                    'sub_total': False,
                    'mass': False,
                    'volume': False,
                    'poids': False,
                    'total': False,
                    'height': False,
                    'transport_means': False,

                }
            )
        else:
            self.update(
                {
                    "volume": self.expedition_id.volume,
                    "qty": self.expedition_id.qty,
                    "prix": self.expedition_id.prix,
                    "sub_total": self.expedition_id.total,
                    'mass': self.expedition_id.mass,
                    "type_colis": self.expedition_id.type_colis,
                    "poids": self.expedition_id.poids,
                    "total": self.expedition_id.total,
                    "height": self.expedition_id.height,
                    "transport_means": self.expedition_id.transport_means,

                }
            )

    @api.model
    def create(self, vals):
        # create returns the newly created record
        rec = super(LogistiqueCommExpe, self).create(vals)
        print(rec.sub_total)
        # if you want to set the value just do this
        rec.total = rec.sub_total  # this will trigger write call to update the field in database
        return rec