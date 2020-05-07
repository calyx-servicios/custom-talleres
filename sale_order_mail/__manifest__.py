# -*- coding: utf-8 -*-
{
    "name": "Sale Order Email Partner",
    "summary": """Agrega el campo email a la sale order y envia el reporte.-""",
    "description": """
        
    """,
    "author": "Calyx",
    "website": "http://www.calyxservicios.com.ar",
    "category": "Sale Order",
    "version": "11.0.1.0.0",
    "depends": ["base", "sale", "account", "sales_team"],
    "data": [
        "data/sale_order_mail_data.xml",
        "views/sale_order_view.xml",
        "wizard/sale_order_mail.xml",
    ],
}
