# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LogistiqueArticle(models.Model):
    _name = 'logistique.article'
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = 'article infos'


    id_article = fields.Char(string='Id_Article', readonly=True, required=True, copy=False,
                            default=lambda self: _('Nouveau'))
    name = fields.Char(string='Nom', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    type = fields.Selection([('service', 'Produit_fini'), ('consumable', 'Produit_non_fini')], "Type d'article", default='service', tracking=True)
    barcode = fields.Char(string='Barcode', tracking=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, required=True, string='Currency')
    sale_price = fields.Monetary(string='Prix de vente', tracking=True)
    tax = fields.Many2one('account.tax', string='Taxes', context={'active_test': False})
    cost = fields.Monetary(string='Cout', tracking=True)
    vente = fields.Monetary(string='Prix', tracking=True)
    total = fields.Monetary(string='Total', tracking=True)
    image = fields.Binary(tracking=True)
    mouvement_produit = fields.Char()
    state = fields.Selection([('brouillon', 'Brouillon'), ('annuler', 'Annuler'), ('enregistre', 'Enregistré')],
                             default="brouillon", string='States')

    initial_quantity = fields.Integer(compute="compute_quantity", string='Quantité initial', readonly=True)
    quantity = fields.Integer(string='Quantite en stock', tracking=True)
    quantity_sold = fields.Integer(string="Quantité vendu", tracking=True, default=0.0)
    # reste_quantity = fields.Integer( string='Quantité restant',tracking=True, default=0.0)


    # function pour calculer quantité initial des quantités
    @api.depends('quantity')
    def compute_quantity(self):
        for record in self:
            record.initial_quantity = record.quantity


    #  #contrainte pour les quantité en stock
    # @api.constrains('initial_quantity','quantity_sold')
    # def _check_quantité_en_stock(self):
    #     for record in self:
    #         if record.quantity_sold > record.initial_quantity:
    #             raise ValidationError("Quantité insufficient en stock")

    # function pour incrementer la quantité vendu

    def increment_vendu(self, achat):
       self.quantity_sold += achat

    # function pour decrementer la quantité de stock
    def decrement_stock_vendu(self, achat):
        self.quantity -= achat

    # function pour appeler une autre view
    def quantity_vendu(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vendu'),
            'view_mode': 'tree',
            'res_model': 'logistique.article',
            'context': "{'create': False}"
        }

    def quantity_restante(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Restant'),
            'view_mode': 'tree',
            'res_model': 'logistique.article',
            'context': "{'create': False}"
        }

    # function pour appeler une autre view
    def product_move(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vendu'),
            'view_mode': 'tree',
            'res_model': 'logistique.article',
            'context': "{'create': False}"
        }

    # function pour appeler une autre view
    def quantity_count(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Quantity'),
            'view_mode': 'tree',
            'res_model': 'logistique.article',
            'context': "{'create': False}"
        }



    @api.model
    def create(self, vals):
        if vals.get('id_article', _('Nouveau')) == _('Nouveau'):
            vals['id_article'] = self.env['ir.sequence'].next_by_code('logistique.article') or _('Nouveau')
        res = super(LogistiqueArticle, self).create(vals)
        return res

    # def name_get(self):
    #     res = []
    #     for rec in self:
        for rec in self:
            name = '[' + rec.id_article + ']'
            result.append((rec.id, name))
        return result

    def action_enregistre(self):
        self.state = 'enregistre'

    def action_brouillon(self):
        self.state = 'brouillon'

    def action_annuler(self):
        self.state = 'annuler'





class LogistiqueMarchandiseCommande(models.Model):
    _name = 'logistique.marchacommande'
    _description = 'commande_article infos'

    marchandise_id = fields.Many2one('logistique.article', string="Marchandise")
    commande_id = fields.Many2one('logistique.produit', string="Commande")
    # name = fields.Char(string='Nom', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    type = fields.Selection([('service', 'Produit_fini'), ('consumable', 'Produit_non_fini')], "Type d'article",default='service', tracking=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'XAF')]).id,
                                  readonly=True, required=True, string='Currency')
    barcode = fields.Char(string='Barcode', tracking=True)
    quantity = fields.Integer(string='Quantite en stock', tracking=True)
    quantity_ok = fields.Integer(string='Quantite', tracking=True)
    sale_price = fields.Monetary(string='Prix de vente', required=True, tracking=True)
    vente = fields.Monetary(string='Prix', readonly=True, tracking=True, compute='_sale_calculates')
    # total = fields.Monetary(string='Total', readonly=True, tracking=True, compute='_total_calculate')

    # function pour appeler une autre view
    def increment_marchandise(self):
        for rec in self:
            rec.marchandise_id.increment_vendu(rec.quantity_ok)

    def decrement_stock_marchandise(self):
        for rec in self:
            rec.marchandise_id.decrement_stock_vendu(rec.quantity_ok)

    @api.depends('sale_price', 'quantity_ok')
    def _sale_calculates(self):
        for r in self:
            if not r.sale_price:
                r.vente = 0.0
            else:
                r.vente = r.sale_price * r.quantity_ok

    #  #contrainte pour les quantité en stock
    @api.constrains('quantity_ok','quantity')
    def _check_quantité(self):
        for record in self:
            if record.quantity_ok > record.quantity:
                raise ValidationError(" La quantité {} en stock insufficient à la quantité {} demander".format(record.quantity,record.quantity_ok))

    # contrainte pour les quantité demander est egal à 0
    @api.constrains('quantity_ok')
    def _check_quantité_ok(self):
        for record in self:
            if record.quantity_ok == 0:
                raise ValidationError( " Veillez mettre une quantité superieur à {}".format(record.quantity_ok))


    # @api.multi
    @api.onchange('marchandise_id')
    def _onchange_marchandise_id(self):
        for rec in self:
            if not rec.marchandise_id:
                rec.update(
                    {
                        # 'name': False,
                        'quantity': False,
                        'description': False,
                        'type': False,
                        'barcode': False,
                        'sale_price': False,
                        'vente': False,
                    }
                )
            else:
                rec.update(
                    {
                        # "name": self.marchandise_id.name,
                        "description": rec.marchandise_id.description,
                        'quantity': rec.marchandise_id.quantity,
                        "type": rec.marchandise_id.type,
                        "barcode": rec.marchandise_id.barcode,
                        "sale_price": rec.marchandise_id.sale_price,
                        "vente": rec.marchandise_id.vente,
                    }
                )




