# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Modifications",
    "summary": """
        This module allow modifications in the sale order form view
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["lucianobaleani"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["base","sale","delivery","sale_pickup_store","sale_order_workflow","sale_contact_partner"],
    'data': [
        "views/sale_order_form_inherited_views.xml"
    ],
}
