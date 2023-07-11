# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Warehouse Restriction",
    "summary": """
        This Module does not allow to create a sale order 
        if any of its lines has "to_design" or "to_quote" fields set in "False" 
        while it has a specific "warehouse_id
            """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["lucianobaleani"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "11.0.1.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["sale","product_attributes"],
}
