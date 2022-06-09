# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Pick Up Store",
    "summary": """
        This module adds the functionality of pick up 
        by stores in sales orders.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "11.0.1.0.0",
    'installable': True,
    'application': False,
    "depends": [
        "sale",
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/sale_store_views.xml',
        'reports/sale_report_templates.xml'
    ],
}