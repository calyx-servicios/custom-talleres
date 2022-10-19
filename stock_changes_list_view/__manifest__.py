# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Changes List",
    "summary": """
        Modify the records that are in red
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["alvarezgianella"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["stock"],
     'data': [
         'views/stock_picking_view.xml',
     ],

}
