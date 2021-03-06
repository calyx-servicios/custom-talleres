# -*- coding: utf-8 -*-
{
    "name": "Sale Order With Advancement Invoices",
    "summary": """Relacion entre la orden de venta y la factura para imputar pagos parciales a la misma.-""",
    "description": """
        
    """,
    "author": "Calyx",
    "website": "http://www.calyxservicios.com.ar",
    "category": "Sale Order",
    "version": "11.0.1.0.1",
    "depends": [
        "base",
        "sale",
        "account",
        "sales_team",
        "sh_message",
        "account_payment_group",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wizard_impute_payment_to_order_view.xml",
        "views/account_payment_group_view.xml",
        "views/sale_order_view.xml",
    ],
}
