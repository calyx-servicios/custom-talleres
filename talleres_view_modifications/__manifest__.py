{
    'name': 'Talleres View Modifications',
    'summary': '''
        Hide fields in the contacts and sales module.
        Modifications in various fields.
    ''',
    'author': "Calyx Servicios S.A.",
    'maintainers': ["DarwinAndrade", "PerezGabriela"],
    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',
    'category': 'Tools',
    'version': '11.0.2.0.0',
    'installable': True,
    'application': False,
    'depends': [
        'crm',
        'base',
        'mrp',
        'sale_order_dates'
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_unbuild_views.xml',
        'views/mrp_workorder.xml',
        'views/stock_move_views.xml',
        'views/stock_scrap_views.xml',
        'wizard/change_production_qty_views.xml',
    ],
}
