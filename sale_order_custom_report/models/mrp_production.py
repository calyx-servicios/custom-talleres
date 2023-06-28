from odoo import models, fields, api
from datetime import timedelta
import dateutil.parser


class MrpProduction(models.Model):
    _inherit = "mrp.production"


    sale_confirmation_date = fields.Datetime(related="sale_id.confirmation_date")
    estimated_days = fields.Integer(default=30)

    compromise_date = fields.Date(string="Commitment Date",
                                    compute="_get_compromise_date",
                                    inverse="_inverse_compromise_date",
                                    readonly=False,
                                    help="This date is the result of the addition between the sale order confirmation day and the estimated days")


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


    @api.multi
    @api.onchange("estimated_days")
    def _onchange_compromise_date(self):
        for order in self:
            date = order.sale_confirmation_date
            if date:
                date = dateutil.parser.parse(date).date()
                new_date = date + timedelta(days=order.estimated_days)
                new_date = new_date.strftime("%Y-%m-%d")
                order.update({"compromise_date": new_date})
            else:
                order.update({"compromise_date": False})


    @api.multi
    @api.depends("estimated_days")
    def _get_compromise_date(self):
        for order in self:
            date = order.sale_confirmation_date
            if date:
                date = dateutil.parser.parse(date).date()
                new_date = date + timedelta(days=order.estimated_days)
                new_date = new_date.strftime("%Y-%m-%d")
                order.update({"compromise_date": new_date})
            else:
                order.update({"compromise_date": False})


    def _inverse_compromise_date(self):
        for order in self:
            date1 = order.sale_confirmation_date
            date2 = order.compromise_date

            if date1:
                if isinstance(date1, str):
                    date1 = dateutil.parser.parse(date1).date()
                else:
                    date1 = date1.date()

            if date2:
                if isinstance(date2, str):
                    date2 = dateutil.parser.parse(date2).date()
                else:
                    date2 = date2.date()

            if date1 and date2:
                total_days = date2 - date1
                order.update({"estimated_days": int(str(total_days.days))})
