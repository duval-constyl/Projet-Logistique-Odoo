# -*- coding: utf-8 -*-
{
    'name': "CamerShipping",  # Module title
    'summary': "Achetez vos marchandises et suivez la jusqu'a la livraison",  # Module subtitle phrase
    'description': """
        Gestion cs_shipping
        ==============
        Achetez, suivez votre commande et faites vos livrer.
    """,  # Supports reStructuredText(RST) format
    'author': "Fotso Duval",
    'website': "http://www.camersoftware.com",
    'category': 'Tools',
    'version': '1.0',
    'depends': ['base','mail'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        # 'data/mail_template.xml',
        'views/logistique_client_views.xml',
        'views/logistique_logisticien_views.xml',
        'views/logistique_article_views.xml',
        # 'views/logistique_commande_views.xml',
        'views/logistique_expedition_views.xml',
        'views/logistique_suivre_views.xml',
        'views/logistique_subscribe_views.xml',
        'views/logistique_note_views.xml',
        'views/logistique_blog_views.xml',
        'views/logistique_quote_views.xml',
        'views/logistique_conteneur_views.xml',
        'views/logistique_livraison_views.xml',
        'views/logistique_transporteur_views.xml',
        'views/logistique_produit_views.xml',
        'views/try_views.xml',
        'views/logistique_delivery_views.xml',
        'report/report.xml',
        'report/logistique_livraison_report_templates.xml',
        'report/logistique_expedition_report_templates.xml',
        'report/logistique_produit_report_templates.xml',
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    'demo': [
        'demo/logistique_client_demo.xml',
        'demo/logistique_article_demo.xml',
        'demo/logistique_transporteur_demo.xml',
        'demo/logistique_logisticien_demo.xml',
        'demo/logistique_blog_demo.xml'
    ],
    'installable': True,
    'images': "icon.jpg",
    'application': True,
    'license': "LGPL-3",
    'sequence': -100
}
