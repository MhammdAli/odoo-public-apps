from odoo import fields, api, models

class ProductCategory(models.Model):
    _inherit = 'product.category'

    low_stock_min_qty = fields.Float("Low Stock Min Qty")

    is_low_stock_applied_on_product_category = fields.Boolean(compute="_compute_is_low_stock_applied_on_product_category")

    def _compute_is_low_stock_applied_on_product_category(self):
        config = self.env['res.config.settings']
        applied_on = config.get_product_quantity_applied_on() 
        for product in self:
            product.is_low_stock_applied_on_product_category = (applied_on == 'category')
