from odoo import models, fields, api

    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_stock_low_quantity = fields.Boolean(
        string="Low Stock Notification",
        implied_group="low_stock_notification.group_stock_low_quantity",
        help="Start Notify users when is there is low stock"
    )

    quantity_type = fields.Selection(
        string="Select Quantity Type",
        selection=[
            ('on_hand',"On Hand"),
            ('forcasted',"Forcasted")
        ],
        default="on_hand",
        config_parameter="stock_low_quantity.quantity_type"
    )

    min_quantity = fields.Float("Minimum Quantity", config_parameter="stock_low_quantity.min_quantity",readonly=False)

    product_quantity_applied_on = fields.Selection(
        string="Applied On",
        selection=[
            ('global','Global'),
            ('individual',"Individual"),
            ('category',"Product Category"),
            ('reordering_rules',"Rreordering Rules")
        ],
        default="global",
        config_parameter="stock_low_quantity.product_quantity_applied_on"
    )

    low_stock_cron_job_xml = fields.Many2one('ir.cron',default=lambda self:self.env.ref('low_stock_notification.mail_low_stock_cron'),store=False,readonly=True)
    low_stock_mail_cron_job_interval_type = fields.Selection(related="low_stock_cron_job_xml.interval_type",readonly=False)
    low_stock_mail_cron_job_interval_number = fields.Integer(related='low_stock_cron_job_xml.interval_number',readonly=False)

    @api.model
    def get_product_quantity_applied_on(self):
        return self.env['ir.config_parameter'].get_param("stock_low_quantity.product_quantity_applied_on")

    @api.model
    def get_product_quantity_based_on(self):
        return self.env['ir.config_parameter'].get_param("stock_low_quantity.quantity_type") 

    @api.model
    def get_global_low_stock_min_qty(self):
        return float(self.env['ir.config_parameter'].get_param("stock_low_quantity.min_quantity"))

    @api.model
    def is_low_stock_qty_enabled(self):
        return self.env.user.has_group('low_stock_notification.group_stock_low_quantity')

    @api.model
    def _is_low_stock_quantity_activated(self):
        """ Return whether the contact names are populated as first and last name or as a single field (name). """
        view = self.env.ref("low_stock_notification.product_template_view_list_inherit", raise_if_not_found=False)
        return view and view.sudo().active
    

    # def set_values(self):
    #     super().set_values()
    #     view_manager = self.env['activation.low.stock.view.manager']
    #     if view_manager.are_low_stock_views_active() != self.group_stock_low_quantity:
    #        view_manager.toggle_low_stock_views(self.group_stock_low_quantity)
    
    @api.model
    def clear_config_parameter(self,target_module):
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        for field in self._fields.values(): 
            field_config_parameter = getattr(field, 'config_parameter', None)
            if field_config_parameter and getattr(field, '_module', None) == target_module: 
                IrConfigParam.search([('key', '=', field_config_parameter)]).unlink()
    
    # @api.model
    # def get_values(self):
    #     res = super().get_values()
    #     res.update(
    #         mass_mailing_split_contact_name=self.env['mailing.contact']._is_name_split_activated(),
    #     )
    #     return res

    # def set_values(self):
    #     super().set_values()
    #     if self._is_low_stock_quantity_activated() != self.group_stock_low_quantity:
    #         self.env.ref(
    #             "low_stock_notification.product_template_view_list_inherit").active = self.group_stock_low_quantity
    #         self.env.ref(
    #             "low_stock_notification.product_template_view_kanban_inherit").active = self.group_stock_low_quantity
    #         self.env.ref(
    #             "low_stock_notification.product_template_view_form_inherit").active = self.group_stock_low_quantity
    