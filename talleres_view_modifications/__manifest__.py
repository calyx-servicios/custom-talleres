{
    'name': 'Talleres View Modifications',
    'summary': '''Hide fields in the contacts and sales module''',
    'version': '11.0.1',
    'category': 'Tools',
    'author': "Calyx",
    'maintainers': ["DarwinAndrade"],
    'website': 'www.calyxservicios.com.ar',
    'license': 'AGPL-3',
    'depends': [
        'sale', 'crm', 'base',
    ],
    'external_dependencies': {
    },
    'data': [
        'view/res_partner_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
