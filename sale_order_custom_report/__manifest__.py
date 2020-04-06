# -*- coding: utf-8 -*-
{
    "name": "Sale Order Custom Report",
    "summary": """
        Reporte de presupuesto con ordenes de trabajo """,
    "description": """
    """,
    "author": "Calyx",
    "website": "http://www.calyxservicios.com.ar",
    "category": "Tools",
    "version": "11.0.1.0.0",
    "depends": ["base", "sale", "mrp", "sale_order_workflow"],
    "data": [
        "report/sale_custom_report.xml",
        "report/sale_custom_template.xml",
        "views/sale_order_view.xml",
    ],
}