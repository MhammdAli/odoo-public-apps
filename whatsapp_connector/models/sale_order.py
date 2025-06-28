from odoo import models, fields, api
 
class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order','whatsapp.mixin']

    
    mobile = fields.Char(related='partner_id.mobile', string='Contact Number')

    def send_whatsapp_message(self,body): 
        """
        Send a WhatsApp message to the partner's mobile number.
        """ 
        return self.send_whatsapp(self.partner_id.mobile, body)
    
    def open_whatsapp_composer(self):  
        action = super().open_whatsapp_composer()
        action['context'].update({
            'default_body': self.env['ir.config_parameter'].get_param('sale.whatsapp_template')
        })
        # _ctx = dict(action['context'])
        # _ctx.update({
        #     'default_body' : self.env['ir.config_parameter'].get_param('sale.whatsapp_template')
        # })
        return action