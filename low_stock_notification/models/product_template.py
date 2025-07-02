from odoo import models, api, fields
from odoo.tools.float_utils import float_round
from functools import wraps
from odoo.exceptions import UserError

def require_group(group_xml_id, default=None):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Supports both single and recordset calls
            if not self.env.user.has_group(group_xml_id):
                return default
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    low_stock_min_qty = fields.Float("Low Stock Min Qty")
    is_low_stock = fields.Boolean("Is Low Stock", compute="_compute_is_low_stock",search="_search_is_low_stock")  
    
    is_low_stock_applied_on_individual = fields.Boolean(compute="_compute_is_low_stock_applied_on_individual")
    
    # search must return domain if None returned it will raise error 'Never leave _search_* without a return.'
    def _search_is_low_stock(self, operator, value):
        if operator not in ['=', '!=']:
            raise UserError(f"Unsupported operator: {operator}")
        if not isinstance(value, bool):
            raise UserError("Expected boolean value")

        config = self.env['res.config.settings']
        based_on = config.get_product_quantity_based_on()
        applied_on = config.get_product_quantity_applied_on()

        quantity_field = {
            'on_hand': 'qty_available',
            'forcasted': 'virtual_available'
        }.get(based_on)

        if not quantity_field:
            raise UserError("Invalid 'Quantity Based On' configuration")

        expected = value if operator == '=' else not value

        if applied_on == 'global':
            min_qty = config.get_global_low_stock_min_qty()
            return [(quantity_field, '<' if expected else '>=', min_qty),('is_storable','=',True)]

        # Optimization: use a smaller initial domain  
        templates = self.search([('is_storable','=',True)])
        matched_ids = []

        for template in templates:
            try:
                min_qty = template.get_low_stock_min_qty()
            except Exception:
                continue  # skip on config issues
            qty = getattr(template, quantity_field, 0.0)
            is_low = qty < min_qty
            if is_low == expected:
                matched_ids.append(template.id)

        return [('id', 'in', matched_ids)] if matched_ids else [('id', '=', 0)]
   
    ########################## low stock color ##########################
    low_stock_color = fields.Char("Low Stock Color",compute="_compute_low_stock_color")

    @api.depends('is_low_stock')
    def _compute_low_stock_color(self): 
        config = self.env['res.config.settings']
        for rec in self:
            if rec.is_low_stock and config.is_low_stock_qty_enabled():
                rec.low_stock_color = 100
            else: 
                rec.low_stock_color = None
    #####################################################################

    def _compute_is_low_stock_applied_on_individual(self):
        config = self.env['res.config.settings']
        applied_on = config.get_product_quantity_applied_on() 
        for product in self:
            product.is_low_stock_applied_on_individual = (applied_on == 'individual')

    @require_group("low_stock_notification.group_stock_low_quantity")
    def get_low_stock_min_qty(self):
        self.ensure_one()
        config = self.env['res.config.settings']
        applied_on = config.get_product_quantity_applied_on()
        rounding = self.uom_id.rounding or 0.01
        
        match applied_on:
            case 'global':
                return float_round(config.get_global_low_stock_min_qty(), precision_rounding=rounding)
            case 'individual':
                return float_round(self.low_stock_min_qty, precision_rounding=rounding)
            case 'category':
                return float_round(self.categ_id.low_stock_min_qty, precision_rounding=rounding)
            case 'reordering_rules':
                return float_round(self.reordering_min_qty, precision_rounding=rounding)
            case _:
                raise UserWarning("You should specify 'Quantity Applied On' field in Stock Settings")

    @require_group("low_stock_notification.group_stock_low_quantity")
    def _is_low_stock_quantity(self):
        if not self.is_storable:
            return None  # or False, depending on use case

        min_qty = self.get_low_stock_min_qty()
        config = self.env['res.config.settings']
        based_on = config.get_product_quantity_based_on()

        match based_on:
            case 'on_hand':
                return self.qty_available < min_qty
            case 'forcasted':
                return self.virtual_available < min_qty
            case _:
                raise UserWarning("Invalid 'Quantity Based On' configuration in Stock Settings")

    @api.depends('qty_available', 'virtual_available')
    def _compute_is_low_stock(self):
        for product in self: 
            product.is_low_stock = product._is_low_stock_quantity()
            

 
    @api.model
    def get_low_stock_products(self):
        """
        Retrieve a list of products that are currently marked as low in stock,
        including their name, internal reference, current stock quantity,
        configured minimum quantity, and the shortage amount.

        Returns:
            dict: {
                'applied_on': str - A label or identifier for how stock rules are applied (from settings),
                'items': list of dicts - Each dict contains:
                    - 'name': str - Product name,
                    - 'code': str - Product internal reference,
                    - 'on_hand': float - Current quantity on hand,
                    - 'min_qty': float - Minimum stock quantity (from logic/config),
                    - 'remaining_qty': float - Shortfall (min_qty - qty_available)
            }
        """
        config = self.env['res.config.settings']
        applied_on = config.get_product_quantity_applied_on()
        based_on = config.get_product_quantity_based_on()

        data = []
        for item in self.search([('is_low_stock','=',True)]):
            min_qty = item.get_low_stock_min_qty()
            data.append({
                'id' : item.id,
                'name' : item.name,
                'description' : item.description,
                'on_hand' : item.qty_available,
                'forcasted' : item.virtual_available,
                'min_qty' : min_qty,
                'remaining_qty' : min_qty - item.qty_available
            })
        
        return LowStockResult(applied_on=applied_on,based_on=based_on,items=data)


class LowStockResult:
    def __init__(self, applied_on,based_on, items):
        self.applied_on = applied_on
        self.items = items
        self.based_on = based_on