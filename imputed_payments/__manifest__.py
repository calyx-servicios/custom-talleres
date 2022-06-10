# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Imputed Payments",
    "summary": """
        This module adds the functionality of posting 
        payments made on an invoice within a sales order.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Accounting",
    "version": "11.0.1.0.0",
    'installable': True,
    'application': False,
    "depends": [
        "account_payment_group",
    ],
}