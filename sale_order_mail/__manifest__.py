# -*- coding: utf-8 -*-
{
    "name": "Sale Order Email Partner",
    "summary": """Agrega un nuevo campo 'Email' a la sale order""",
    "description": """
    """,
    "author": "Calyx",
    "website": "http://www.calyxservicios.com.ar",
    "category": "Sale Order",
    "version": "11.0.1.0.0",
    "depends": [
        "base",
        "sale",
        "account",
        "sales_team",
        "sale_order_workflow",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sale_order_mail_data.xml",
        "views/sale_order_view.xml",
        "wizard/sale_order_mail.xml",
    ],
}
