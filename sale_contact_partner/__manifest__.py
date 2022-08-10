# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Contact Partner",
    "summary": """
        This module add the field customer and zone. And also makes the fields Zone and Email required.
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
    "depends": ["base","contacts","sale","sale_order_mail","sale_order_workflow"],
    'data': [
        "views/res_partner_form_inherited_views.xml",
        "views/sale_order_form_inherited_view.xml",
    ],
}
