from odoo import models, fields, api    
from urllib.parse import urlencode

 
class MailWhatsapp(models.TransientModel):
    _name = 'mail.whatsapp'
    _transient_max_count = 1
    _transient_max_hours = 0.1
 
    model = fields.Char('Related Document Model') 
    res_id = fields.Many2oneReference('Related Document ID', model_field='model')

    mobile = fields.Char('Mobile')
    body = fields.Text("Body", 
        sanitize_style=True, 
        sanitize_tags=False,
        render_engine='template_inline',  
        render_options={'post_process': True},
        prefetch=True, 
        translate=True)

    auto_delete = fields.Boolean("Auto Delete",default=False)
    
    def _render_template(self,add_context = None):  
        _rendered_template = self.env['mail.render.mixin']._render_template_inline_template(
            self.body,
            self.model,
            [self.res_id],
            add_context=add_context
        )
        return _rendered_template[self.res_id]

    @api.model
    def _parse_message(self,add_context=None):  
        query_params = {
            'phone': self.mobile,
            'text': self._render_template(add_context),
        }
        return  urlencode(query_params)

     
    def send_whatsapp(self,add_context=None):  
        # Prepare the action to open WhatsApp with the encoded query parameters
        if not self.mobile:
            raise ValueError("Mobile number is required to send a WhatsApp message.") 

        _whatsapp_url = self.env['ir.actions.act_url']._for_xml_id('whatsapp_connector.action_whatsapp_send_url')
        _whatsapp_url['url'] += f'?{self._parse_message(add_context)}'
        
        # action = {  
        #     'type': 'ir.actions.act_url',
        #     'url': f'https://api.whatsapp.com/send?{self._parse_message(add_context)}',
        #     'target': 'new',
        # }
        
        if self.auto_delete : 
            self.sudo().unlink()
            
        return _whatsapp_url 
    