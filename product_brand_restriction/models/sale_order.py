from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    template_id = fields.Many2one('product.template', string='Product')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.product_id', 'order_line.template_id', 'order_line')
    def _get_brands(self):
        for order in self:
            brands = []
            for line in order.order_line:
                if line.template_id and line.template_id.product_brand_id:
                    brands.append(line.template_id.product_brand_id.id)
            order.brand_ids=brands
            

    brand_ids = fields.Many2many(
        'product.brand', 'sale_brand_rel','order_id', 'brand_id', 'Brands',compute=_get_brands, store=True)
