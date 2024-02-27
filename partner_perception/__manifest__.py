# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Perceptions",
    "summary": """
        This module add taxes in partner on invoice
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["GeorginaGuzman", "PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Stock",
    "version": "13.0.3.0.1",
    "installable": True,
    "application": False,
    "depends": [
        "l10n_ar_account_withholding",
        "l10n_ar",
        "account"
    ],
    "data": [
        "views/account_move_view.xml"
    ],
}