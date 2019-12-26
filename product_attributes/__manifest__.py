# -*- coding: utf-8 -*-
{
    'name': "Product Attributes",
    'summary': """
        Product Attributes Management """,

    'description': """
        Another Way to handle products attributes
    """,
    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",
    'category': 'Sales',
    'version': '11.0.1.0.0',
    'depends' : [
        'sale',
        'base_fontawesome',
        ],

    'data': [
        'views/sale_order_view.xml',
        'wizard/sale_custom_product.xml',
    ],
}
