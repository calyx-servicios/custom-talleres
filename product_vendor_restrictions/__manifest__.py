# -*- coding: utf-8 -*-
#        - Vendor Group creation.
#        - Record Rule that avoid a Vendor to see Purchasable Products.
#        - Purchasable Boolean on Product Template and Product Variant Form View hided of the Vendor Group.
#        - Add the Permission to Vendor to create and update Products.
#        - Modifies the purchase_ok field to be False as default.

{
    'name': "Product Vendor Restrictions",
    'summary': """Users added to the Vendor Group can't get access to Purchasable Products.
    """,
    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",
    'license': "LGPL-3",
    'category': 'Sales',
    'version': '11.0.1.0.0',
    'depends' : [
        'base',
        'stock',
        'sale',
        'product',
    ],
    'data': [
        'security/product_security.xml',
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/product_product_view.xml'
    ],
    'installable': True,
    'auto_install': False
}