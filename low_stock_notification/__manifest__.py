# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Low Stock Notification',
    'summary': 'Automatically notify responsible users when product stock is low.',
    'version': '1.0',
    'author': 'Mhmad Harb',
    'maintainer': 'Mhmad Harb',
    'category': 'Inventory/Inventory',
    'description': """
Low Stock Notification
=======================
This module notifies responsible users when product quantities fall below a defined threshold.

Features:
---------
- Set minimum stock levels per product or category.
- Automatic email notifications for low stock.
- Scheduled actions to check stock regularly.
    """,
    'depends': ['base',"stock"],
    'data': [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/product_template.xml",
        "views/product_category.xml",
        "data/mail_template_data.xml",
        "views/mail_low_stock_cron_job.xml"
    ], 
    "images" : ['static/description/banner.gif'],
    'installable': True,
    'license': 'LGPL-3', 
    'uninstall_hook': 'uninstall_hook',
}
