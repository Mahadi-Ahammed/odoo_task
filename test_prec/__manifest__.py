{
    'name': 'Test Prec',
    'version': '1.0',
    'category': 'crm',
    'summary': 'Test Prec',
    'description': """Test Prec""",
    'data': [
        'security/ir.model.access.csv',
        'views/my_custom_views.xml',
        'data/res_users.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'test_prec/static/src/css/map_view_style.scss',
            'test_prec/static/src/js/map_view_widget.js',
            'test_prec/static/src/xml/map_view_template.xml',
            'test_prec/static/src/xml/chatbot_systray.xml',
            'test_prec/static/src/js/chatbot_systray.js',
        ],
    },
    'depends': ['base', 'web', 'mail'],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}