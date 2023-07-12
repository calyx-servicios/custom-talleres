{
    "name": "Tags Report",
    "summary": """
        This module adds the tags to
        the manufacturing report.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Manufacturing",
    "version": "11.0.1.2.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["mrp","product_attributes", "web"],
    "data": [
        "report/report_tags.xml",
        "report/mrp_production_reports.xml",
        "views/product_attribute_view.xml"
    ]
}
