from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def print_custom_sale_report(self):
        """
            Print the report based in the workcenter routing BOM
        """
        self.ensure_one()
        if self.sale_id:
            self.sale_id.create_attach_img()
            action = self.env.ref(
                "sale_order_custom_report.action_sale_order_custom_report"
            )
            vals = action.read()[0]
            context = vals.get("context", {})
            context["active_id"] = self.sale_id.id
            context["active_ids"] = [self.sale_id.id]
            vals["context"] = context

            return vals
