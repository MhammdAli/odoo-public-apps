from odoo import models, api
import logging

_logger = logging.getLogger(__name__)
    
class mail_low_stock(models.AbstractModel):
    _name = 'mail.low.stock.message'
    _description = 'Send Low Stock Notification Email'

    @api.model
    def send_low_stock_mail(self):
        """
        Sends a low stock notification email using the predefined email template
        if there are any products marked as low stock.
        """
        low_stock_result = self.env['product.template'].get_low_stock_products()
       
        # Load the email template
        template = self.env.ref('low_stock_notification.low_stock_notification', raise_if_not_found=False)
        if not template:
            _logger.warning(
                "Low stock notification email template not found: XML ID 'low_stock_notification.low_stock_notification'. "
                "Please ensure the template is defined and accessible in the database."
            )
            return
        
        if not low_stock_result.items:
            return
            
        # Build context for email rendering
        ctx = dict(self.env.context or {})
        ctx.update({
            'items': low_stock_result.items,
            'applied_on': low_stock_result.applied_on,
            'based_on' : low_stock_result.based_on
        })
        
        # Send email to the company (res.company record)
        company = self.env.company
        template.with_context(ctx).send_mail(company.id, force_send=True)
