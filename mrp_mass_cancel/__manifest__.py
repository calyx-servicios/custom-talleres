# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "MRP Mass Cancel",
    "summary": """
        This module helps you to cancel in mass mrp orders in list view
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["ParadisoCristian"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Mrp",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["mrp"],
    'data': [
        'wizard/wizard_mrp_mass_cancel_views.xml',
        'views/mrp_production_views.xml',
    ],
}
