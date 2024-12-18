{
    'name': 'Bista Debuging Challenge',
    'version': '1.0',
    'category': 'crm',
    'summary': 'Bista Debuging Challenge',
    'description': """Bista Debuging Challenge""",
    'depends': ['sale', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/commission_report.xml',
        
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}