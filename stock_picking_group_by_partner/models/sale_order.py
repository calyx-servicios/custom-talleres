from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    picking_ids = fields.Many2many("stock.picking", string="Transfers", copy=False)

    def action_cancel(self):
        for sale_order in self:
            # change the context so we can intercept this in StockPicking.action_cancel
            super(
                SaleOrder, sale_order.with_context(cancel_sale_id=sale_order.id)
            ).action_cancel()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_group_vals(self):
        return {
            'name': self.order_id.name,
            'move_type': self.order_id.picking_policy,
            'sale_id': self.order_id.id,
            'partner_id': self.order_id.partner_shipping_id.id,
            'carrier_id': self.order_id.carrier_id.id,
        }
