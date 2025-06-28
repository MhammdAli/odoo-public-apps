from odoo import models, fields, api
 

class whatsappComposer(models.TransientModel):
    _name = 'mail.whatsapp.composer' 
    _description = 'WhatsApp Composer'
 
    body = fields.Text("Body")
        
    # partner_id = fields.Many2one('res.partner', string='Recipient', required=True,domain="[('mobile', '!=', False)]")
    
    recepiant_id =  fields.Many2one('res.partner', string='Recipient', required=True,domain="[('mobile', '!=', False)]")
    
    mobile = fields.Char(related='recepiant_id.mobile', string='Contact Number', readonly=True)
    partner_avatar = fields.Binary(related='recepiant_id.image_512', string='Avatar', readonly=True)
     
    model = fields.Char('Related Document Model',default='res.partner',readonly=True,store=False) 
    res_id = fields.Many2oneReference('Related Document ID', model_field='model',default=lambda l:l.recepiant_id.id,readonly=True,store=False)

    
    def send_whatsapp_message(self): 
        # Use the send_whatsapp_message method from partner
        # return self.partner_id.send_whatsapp_message(self.body)
        print(self._context) 
        return self.env['mail.whatsapp'].create({
            'body' : self.body,
            'res_id' : self.res_id,
            'model' : self.model,
            'mobile' : self.mobile,
            'auto_delete' : True
        }).send_whatsapp()