# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Advance in Report",
    "summary": """
        This module adds the functionality of advance field in sales orders.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Garaceliguzman"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "11.0.1.0.1",
    'installable': True,
    'application': False,
    "depends": [
        "sale",
    ],
    'data': [
        'reports/sale_report_templates.xml'
    ],
}