# __manifest__.py
{
    'name': 'beauty_salon',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Manage beauty salon operations',
    'description': """
        beauty_salon
        =======================
        This module helps beauty salons manage:
        - Customer records
        - Service catalog
        - Price packages
        - Appointment scheduling
        - Staff management
    """,
    'depends': ['base', 'mail', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_views.xml',
        'views/service_views.xml',
        'views/package_views.xml',
        'views/appointment_views.xml',
        'views/staff_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}