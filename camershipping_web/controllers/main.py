# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# from odoo import base64


class HomePage(http.Controller):

    @http.route('/', auth='public', website=True, type="http",method='POST')
    def index(self, **post):
        blogs = http.request.env['logistique.blog'].search([])

        if post.get('name'):
            name = post.get('name')
            mail = post.get('mail')
            phone = post.get('phone')
            note = post.get('note')

            request.env['logistique.free'].sudo().create({
                'name': name,
                'mail': mail,
                'phone': phone,
                'note': note,
            })

        if post.get('name'):
            name = post.get('name')
            mail = post.get('mail')

            request.env['logistique.subscribe'].sudo().create({
                'name': name,
                'mail': mail,
            })

            return request.redirect('/?submitted=1')
        return request.render('camershipping_web.home', {
            'blogs': blogs,
            'message': request.env['logistique.free'].search([]),
            'message': request.env['logistique.subscribe'].search([]),
            'submitted': post.get('submitted', False)
        })

# route pour la page d'enregistrement
    @http.route('/login', auth='public', website=True, type="http", csrf=False )
    def login(self, **post):
        countries = http.request.env['res.country'].sudo().search([])
        if post.get('name'):
            name = post.get('name')
            surname = post.get('surname')
            mail = post.get('mail')
            country = post.get('country')
            password = post.get('password')
            confirm_password = post.get('confirm_password')
            telephone = post.get('telephone')
            adresse = post.get('adresse')

            request.env['logistique.client'].sudo().create({
                'name': name,
                'surname': surname,
                'mail': mail,
                'country': country,
                'password': password,
                'confirm_password': confirm_password,
                'telephone': telephone,
                'adresse': adresse,
            })

            # request.env['res.users'].sudo().create({
            #     'name': name,
            #     'login': mail,
            #     'password': password,
            #     'country': country,
            #     'zipcode': adresse,
            # })
            return request.redirect('/login?submitted=1')
        return request.render('camershipping_web.login', {
            'countries': countries,
            'message': request.env['logistique.client'].search([]),
            'submitted': post.get('submitted', False)
        })

    @http.route('/tracking', auth='public', website=True, type="http")
    def tracking(self):
        return request.render('camershipping_web.tracking')


    @http.route('/cart-shop', auth='public', website=True, type="http")
    def cart(self):
        return request.render('camershipping_web.cart-shop')

    @http.route('/expedition', auth='public', website=True, type="http", csrf=False)
    def expedition(self, **post):
        countries = http.request.env['res.country'].sudo().search([])
        context={
            'countries': countries,
        }
        if post.get('phone'):
            names = post.get('names')
            phone = post.get('phone')
            email = post.get('email')
            card_id = post.get('card_id')
            adresse = post.get('adresse')
            country_id = post.get('country_id')
            city = post.get('city')
            zip = post.get('zip')

            type_colis = post.get('type_colis')
            transport_means = post.get('transport_means')
            qty = post.get('qty')
            mass = post.get('mass')
            volume = post.get('volume')
            height = post.get('height')

            request.env['logistique.expedition'].sudo().create({
                'names': names,
                'phone': phone,
                'email': email,
                'card_id': card_id,
                'adresse': adresse,
                'nationality': country_id,
                'city': city,
                'zip': zip,
                'expedition_ids.type_colis': type_colis,
                'expedition_ids.transport_means': transport_means,
                'expedition_ids.qty': qty,
                'expedition_ids.mass': mass,
                'expedition_ids.volume': volume,
                'expedition_ids.height': height,
            })
            #
            # request.env['logistique.commexpe'].sudo().create({
            #     'type_colis': type_colis,
            #     'transport_means': transport_means,
            #     'qty': qty,
            #     'mass': mass,
            #     'volume': volume,
            #     'height': height,
            # })

        if post.get('type_coliss'):
            type_coliss = post.get('type_coliss')
            transport_meanss = post.get('transport_meanss')
            qtys = post.get('qtys')
            masss = post.get('masss')
            volumes = post.get('volumes')
            heights = post.get('heights')

            request.env['logistique.quote'].sudo().create({
                'type_coliss': type_coliss,
                'transport_meanss': transport_meanss,
                'qtys': qtys,
                'masss': masss,
                'volumes': volumes,
                'heights': heights,
            })

        return request.render('camershipping_web.expedition', context,{
            'message': request.env['logistique.expedition'].search([]),
            # 'message': request.env['logistique.commexpe'].search([]),
            'message': request.env['logistique.quote'].search([]),
            'submitted': post.get('submitted', False)
        })


    @http.route('/store', auth='public', website=True, type="http")
    def store(self, **kw):
        articles = http.request.env['logistique.article'].search([])
        return request.render('camershipping_web.store',{
            'articles' : articles
        })

