# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{

    "name": "Picking Validation",
    "summary": """
        This Module will automatically print the picking once it is validated
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["lucianobaleani"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["stock","sale_order_workflow","print_check_control"],
    "data":["views/stock_picking_inherited_views.xml"]
}
