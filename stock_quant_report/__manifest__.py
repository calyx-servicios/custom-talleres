# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Quant Report",
    "summary": """
        Stock Quant Report.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["mparadiso233"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "13.0.1.0.0",
    "installable": True,
    "application": False,
    "depends": [
        "stock"
    ],
    "data": [
        "views/stock_quant_views.xml",
        "views/product_product_views.xml"
    ],
}
