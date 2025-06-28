from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    whatsapp_model = fields.Char('Whatsapp Model',default="sale.order",store=False,readonly=True)
    whatsapp_template_note = fields.Char('Whatsapp Template',config_parameter='sale.whatsapp_template')