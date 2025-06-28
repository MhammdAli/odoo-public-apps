from odoo import models, api    
 
class WhatsappMixin(models.AbstractModel):
    _name = 'whatsapp.mixin'
  
    @api.model
    def send_whatsapp(self, phone, body):  
        # Prepare the action to open WhatsApp with the encoded query parameters
        mail_whatsapp = self.env['mail.whatsapp'].create({
            'model' : self._name,
            'res_id' : self.id,
            'body' : body,
            'mobile' : phone,
            'auto_delete' :  True
        }) 
        return mail_whatsapp.send_whatsapp() 
    
    def open_whatsapp_composer(self):  
        """
        Open the WhatsApp composer with the specified partner and message body.
        """   
        action = self.env['ir.actions.act_window']._for_xml_id('whatsapp_connector.whatsapp_composer_action')  
        _ctx = dict(self.env.context) 
        _ctx.update({
            'default_model' : self._name,
            'default_res_id' : self.id,
            # 'default_partner_id' : self.id # we need to remove ot when we khow the issue of passing it from button and act window of the composer
        })
        action['context'] = _ctx  
        return action

# class WhatsappMixin(models.AbstractModel):
#     _name = 'whatsapp.mixin'

#     def _render_template(self,body):  
#         _rendered_template = self.env['mail.render.mixin']._render_template_inline_template(
#             body,
#             self._name,
#             [self.id]
#         )
#         return _rendered_template[self.id]

#     @api.model
#     def _parse_message(self,phone, body):  
#         query_params = {
#         'phone': phone,
#         'text': self._render_template(body),
#         }
#         return  urlencode(query_params)

#     @api.model
#     def send_whatsapp(self, phone, body):  
#         # Prepare the action to open WhatsApp with the encoded query parameters
#         if not phone:
#             raise ValueError("Mobile number is required to send a WhatsApp message.") 

#         action = {  
#             'type': 'ir.actions.act_url',
#             'url': f'https://api.whatsapp.com/send?{self._parse_message(phone, body)}',
#             'target': 'new',
#         }

#         return action 
    
#     @api.model
#     def open_whatsapp_composer(self,active_ids):  
#         """
#         Open the WhatsApp composer with the specified partner and message body.
#         """  
#         action = self.env['ir.actions.act_window']._for_xml_id('whatsapp_connector.whatsapp_composer_action') 
#         # _ctx = dict(self.env.context)  # Merge the current context with the provided context
#         # _ctx.update({
#         #     'partner_readonly': True,
#         #     'default_partner_id': 22,
#         # }) 
#         # action['context'] = _ctx
#         return action