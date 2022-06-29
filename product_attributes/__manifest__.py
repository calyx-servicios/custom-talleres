# -*- coding: utf-8 -*-
{
    "name": "Product Attributes",
    "summary": """
        Product Attributes Management """,
    "description": """
        Another Way to handle products attributes
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["CristianParadiso", "PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "11.0.3.2.0",
    "installable": True,
    "application": False,
    "depends": ["sale", "base_fontawesome", "product"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/product_view.xml",
        "wizard/sale_custom_product.xml",
    ],
}
