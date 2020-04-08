# -*- coding: utf-8 -*-
{
    "name": "Sale Order Workflow",
    "summary": """""",
    "description": """

    """,
    "author": "Calyx",
    "website": "http://www.calyxservicios.com.ar",
    "category": "Sale",
    "version": "11.0.1.0.0",
    "depends": [
        "base",
        "sale",
        "account",
        "mrp",
        "sale_mrp",
        "mrp_sale_info",
        "product_attributes",
        "sale_order_advancement",
        "web_tree_dynamic_colored_field",
        "web_notify",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/mrp_production_view.xml",
        "views/stock_picking_view.xml",
        "views/sale_order_design.xml",
        "data/product_template_data.xml",
    ],
}
