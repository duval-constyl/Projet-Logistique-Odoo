# -*- coding: utf-8 -*-
{
    'name': "CamerShipping Web",  # Module title
    'summary': "Achetez vos marchandises et suivez la jusqu'a la livraison",  # Module subtitle phrase
    'description': """
    Gestion cs_shipping_web
    ==============
    Achetez, suivez votre commande et faites vos livrer .
        """,  # Supports reStructuredText(RST) format
    'author': "Camer Software",
    'website': "www.camersoftware.com",
    'category': 'Shipping',
    'version': '1.0',
    'depends': ['base','website', 'camershipping'],

    'data': [
        'views/header.xml',
        'views/home.xml',
        'views/login.xml',
        'views/cart.xml',
        'views/store.xml',
        'views/tracking.xml',
        'views/expedition.xml'
    ],

    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],

    'installable': True,
    'images': "icon.png",
    'application' : True,
    'license' : "LGPL-3",
    'sequence' : -100
}
