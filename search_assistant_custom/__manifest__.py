{
    "name": "Search Assistant (Custom)",
    "summary": """
        Custom search features for sales and purchase orders (Customizations)
    """,
    "author": "Calyx Servicios S.A.",
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Accounting",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["base",
                "search_assistant"],
    'data': ['views/sale_order_view.xml',
             'wizard/search_assistant_wizard_view.xml',
     ],
    'installable': True,
    'auto_install': False,
    #'post_init_hook': 'copy_date_order_post_init_hook',
}
