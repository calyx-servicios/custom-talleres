# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Design Production",
    "summary": """
        This module allow to classificate the production orders that come from design orders
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["lucianobaleani","PerezGabriela"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "MRP",
    "version": "11.0.3.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["sale_order_workflow"],
    'data': [
        "views/mrp_production_inherited_views.xml",
        "views/sale_order_view.xml",
    ],
}
