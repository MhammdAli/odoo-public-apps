
from odoo import models, fields, api
 
class Partner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner','whatsapp.mixin']

 
    def send_whatsapp_message(self,body):
        """
        Send a WhatsApp message to the partner's mobile number.
        """  
        return self.send_whatsapp(self.mobile, body)
    
 