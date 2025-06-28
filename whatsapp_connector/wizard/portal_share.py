from odoo import models, fields, api
from urllib.parse import quote

default_template ="""
Dear {{object.partner_id.name}},
Greetings from {{user.company_id.name}}!
{{object._description}} / {{object.name}}
You have been invited to access {{object._description}}.
Click the link below to access:
{{share_link}}
""" 

class PortalShare(models.TransientModel): 
    _inherit = 'portal.share'

    
    share_method = fields.Selection(
        selection=[('mail', 'Mail'),('whatsapp', 'WhatsApp')],
        string='Sharing Method',
        default='mail',
        help="Select the method to share the portal link."
    ) 
    mobile = fields.Char(
        "Mobile Number",
        help="Mobile number of the customer to send the WhatsApp message to.",
        compute='_compute_mobile',
        store=True,
        readonly=False,
        required=True
    ) 
    

    customer_id = fields.Many2one('res.partner',
        string='Customer',
        domain="[('mobile', '!=', False)]",
        help="Select the customer to send the WhatsApp message to.",
        required=True,
        compute='_default_partner',
        readonly=False,
        store=True
    )
    
    body = fields.Text("Body", 
        sanitize_style=True, 
        sanitize_tags=False,
        render_engine='qweb',  
        render_options={'post_process': True},
        prefetch=True, 
        translate=True,
        default=default_template)

    @api.depends('resource_ref')
    def _default_partner(self):
        if self.resource_ref.partner_id.mobile:
            self.customer_id = self.resource_ref.partner_id

    @api.depends('customer_id')
    def _compute_mobile(self):
        for rec in self:
            if rec.customer_id:
                rec.mobile = rec.customer_id.mobile
            else:
                rec.mobile = False

    def action_send_whatsapp(self):    
        mail_whatsapp = self.env['mail.whatsapp'].create({
            'body' : self.body,
            'mobile' : self.mobile,
            'model' : self.res_model,
            'res_id' : self.res_id,
            'auto_delete' : True
        })
        return mail_whatsapp.send_whatsapp({
            'share_link' : self.share_link,
            'portal_record' : self
        }) 
      

    def action_send_mail(self): 
        if self.share_method == 'whatsapp':
            return self.action_send_whatsapp()  
        else:
            return super(PortalShare, self).action_send_mail()  