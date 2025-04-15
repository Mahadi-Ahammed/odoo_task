{
    'name': 'BayVista Real Estate',
    'version': '1.0',
    'summary': 'Real Estate Management Module',
    'description': 'This module manages real estate properties, users, and related data.',
    'author': 'Anamika',
    'category': 'Real Estate',
    'depends': ['base', 'web', 'mail', 'project_todo', 'contacts', 'project', 'mass_mailing', 'survey', 'hr', 'utm', 'website'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',   
        'data/res_users.xml',
        'data/website_menu_data.xml',
        'data/properties_page.xml',
        'views/property_views.xml',
        'views/user_views.xml',
        'views/menus.xml',
        'views/menu_hide.xml',
        'views/vista_property_stage_view.xml',
	    'views/properties_details.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'bayvista_realestate/static/src/scss/website_view.scss',
            'bayvista_realestate/static/src/js/image_slider.js',
            'bayvista_realestate/static/src/js/property_details.js',
            'bayvista_realestate/static/src/js/user_profile.js',
        ],
        
        'web.assets_backend': [
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'bayvista_realestate/static/src/css/map_view_style.scss',
            'bayvista_realestate/static/src/js/map_view_widget.js',
            'bayvista_realestate/static/src/xml/map_view_template.xml',
            'bayvista_realestate/static/src/css/user_kanban.css',
            'bayvista_realestate/static/src/js/chatbot_systray.js',
            'bayvista_realestate/static/src/xml/chatbot_systray.xml',
            'bayvista_realestate/static/src/js/chat_window.js',

        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
