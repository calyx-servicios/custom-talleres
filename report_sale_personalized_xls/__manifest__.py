# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "sale xls report",
    "summary": """
        This module allows you to add a new custom report on sales
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Garaceliguzman",],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "MRP",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["sale","sale_order_workflow", "report_xlsx"],
    'data': [
        "report/report_xls_sale_view.xml",
    ],
}
