from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    with_design = fields.Boolean(string="With design", default=False)

    def action_to_design(self):
        res = super(SaleOrder, self).action_to_design()
        if res == True:
            self.write({"with_design": True})
        else:
            self.write({"with_design": False})
        return res

    @api.multi
    def action_confirm_new(self):
        res = super(SaleOrder, self).action_confirm_new()
        for order in self:
            products = []
            for line in order.order_line:
                if line.to_design == True:
                    products.append(line.product_id.id)
                if order.production_count != 0 and order.with_design:
                    for mrp in order.production_ids:
                        if mrp.product_id.id in products:
                            mrp.write({"from_design": "mrp_from_design"})
        return res
                            