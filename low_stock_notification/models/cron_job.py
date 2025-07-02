from odoo import api, models
from odoo.exceptions import ValidationError

class CronJob(models.Model):
    _inherit = 'ir.cron'

    @api.ondelete(at_uninstall=False)
    def _prevent_low_stock_cron_delete(self):
        cron = self.env.ref('low_stock_notification.mail_low_stock_cron', raise_if_not_found=False)
        if cron and cron.id in self.ids:
            raise ValidationError((
                "This scheduled action is required for low stock notifications and cannot be deleted."
            ))
            