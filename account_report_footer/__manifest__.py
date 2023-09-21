# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Report Footer",
    "summary": """
    This Module fix the account report footer
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["lucianobaleani"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Localization/Argentina",
    "version": "11.0.1.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["l10n_ar_aeroo_einvoice"],
    "data": [
        "invoice_report.xml",
    ],
}
