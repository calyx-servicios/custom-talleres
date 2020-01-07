# -*- coding: utf-8 -*-
{
    'name': "Sale Order Workflow",
    'summary': """""",

    'description': """

    """,
    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",
    'category': 'Sale',
    'version': '11.0.1.0.0',
    'depends' : [
        'base',
        'sale',
        'account',
        'sale_mrp',
        'mrp_sale_info',
        'product_attributes',
        'sale_order_advancement'
        ],
    'data': [
        'views/sale_order_view.xml',
        'views/mrp_production_view.xml',
        ],
}
