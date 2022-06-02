# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Picking Details',
    'summary': '''
        This module adds fields extra in stock picking
    ''',
    'author': "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    'license': 'AGPL-3',
    'category': 'Stock',
    'version': '11.0.2.0.0',
    'installable': True,
    'application': False,
    'depends': [
        'stock','sale','sale_order_advancement'
    ],
    'data': [
        'views/stock_view.xml',
        'reports/report_delivery_document.xml',
    ],
}