from odoo import models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.constrains("warehouse_id")
    def check_warehouse_sale_order(self):
        for rec in self:
            if rec.state == "draft":
                context = [
                    ("order_id", "=", rec.id),
                    ("to_quote","=", False),
                    ("to_design","=", False)
                ]
                products = self.env["sale.order.line"].search(context)
                if products:
                    if rec.warehouse_id.name == "Taller":
                        raise UserError(_("You cannot use this warehouse. If there are not products with the to quote or to design actives"))
