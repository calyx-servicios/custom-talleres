# -*- coding: utf-8 -*-
{
    'name': "Product Brand Restriction",
    'summary': """
        Product Brand Domain Restrictions """,

    'description': """
        Product Brand Domain Restrictions
    """,
    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",
    'category': 'Sales',
    'version': '11.0.1.0.0',
    'depends' : [
        'product_attributes',
        'product_brand',
        'sale',
        ],
    'data': [
        'views/user_view.xml',
        'views/sale_order_view.xml',
        'views/product_view.xml',
        'reports/sale_report.xml',
    ],
}
