{
    'name': 'Whatsapp Connector',
    'version': '18.0.1.0.0',
    'category': 'services/whatsapp',
    'summary': 'Whatsapp Connector App for Odoo',
    'description': """
📱 **WhatsApp Connector for Odoo**  
Enhance your business communication with a powerful and beautifully designed WhatsApp integration for Odoo.  

This module allows users to send WhatsApp messages directly from the Odoo interface, offering a seamless messaging experience integrated into your existing workflow. The connector works with the `res.partner` model, enabling communication with customers and partners using their mobile numbers.
    """,
    'depends': ['base',"mail","sale",'contacts','account'],
    'data': [
        "wizard/whatsapp_composer.xml",
        "views/res_partner.xml", 
        "views/sale_order_views.xml",
        "security/ir.model.access.csv",
        "wizard/portal_share.xml",
        "views/mail_whatsapp.xml",
        "views/res_config_settings.xml"
    ],
    'assets' : {
        'web.assets_backend': [
            "whatsapp_connector/static/src/js/**/*",
            "whatsapp_connector/static/src/xml/**/*",
            "whatsapp_connector/static/src/scss/**/*",
        ]
    },
    'installable': True,
    'auto_install': True,
    'application': False,
    'license': 'LGPL-3'
}
