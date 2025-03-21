{
    'name': 'Real Estate',
    'author': 'jo',
    'version': '17.0.0.1.0',
    'description': 'This is Real Estate',
    'license': 'LGPL-3',  # Added license
    'depends': ['base', 'web','sale_management', 'account', 'mail', 'contacts'],
     'data': [
    'security/security.xml', 
    'security/ir.model.access.csv', 
    'data/sequence.xml',
    'views/property_view.xml',  
    'views/base_menu.xml',
    'views/owner_view.xml',
    'views/tag_view.xml',
    'views/sale_order_view.xml',
    'views/res_partner.xml',
    'views/building_view.xml',
    'views/property_history_view.xml',
    'views/account_move_view.xml',
    'wizard/change_state_wizard_view.xml',
    'reports/property_report.xml',
    'reports/property_template.xml',
],
"assets": {
    "web_assets_backend": ["/app_one/static/src/css/property.css"],
    "web_report_assets_common": ["/app_one/static/src/css/font.css"]
  },
    'installable': True,  # Ensure it's installable
    'auto_install': False,  # Prevent auto-installing
    'application': True,
}
