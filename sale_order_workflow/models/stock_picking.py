# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import datetime
import logging

_logger = logging.getLogger(__name__)


class stockPicking(models.Model):
    _inherit = "stock.picking"

    freight = fields.Float(string="Freight")
    placement = fields.Float(string="Placement")

    invoice_freight_placement_id = fields.Many2one(
        "account.invoice", string="Invoice"
    )
    freigt_placement_status = fields.Selection(
        [("invoiced", "Invoiced"), ("no", "Nothing in invoice")],
        string="Invoice Status",
        default="no",
    )

    @api.multi
    @api.onchange("freight", "placement")
    def _onchange_freight_placement(self):
        for rec in self:
            if rec.sale_id:
                rec.sale_id.write(
                    {"freight": rec.freight, "placement": rec.placement}
                )

    @api.multi
    def create_invoice_fregiht_placement(self):
        for rec in self:
            vals = {}
            invoice_obj = self.env["account.invoice"]
            product_obj = self.env["product.product"]
            freight = product_obj.search(
                [("freight", "=", True)], limit=1
            )
            placement = product_obj.search(
                [("placement", "=", True)], limit=1
            )
            vals = {
                "partner_id": rec.partner_id.id,
                "team_id": rec.sale_id.team_id.id,
                "origin": rec.name,
                "date_invoice": datetime.datetime.now().date(),
            }

            invoice_id = invoice_obj.create(vals)
            if freight:
                accounts = (
                    freight.product_tmpl_id.get_product_accounts()
                )
                rec._create_invoices_lines(
                    accounts,
                    freight,
                    rec.freight,
                    rec.name,
                    invoice_id.id,
                )
            if placement:
                accounts = (
                    placement.product_tmpl_id.get_product_accounts()
                )
                rec._create_invoices_lines(
                    accounts,
                    placement,
                    rec.placement,
                    rec.name,
                    invoice_id.id,
                )
            rec.freigt_placement_status = "invoiced"
            rec.invoice_freight_placement_id = invoice_id.id

    def _create_invoices_lines(
        self, accounts, freight, precio, origin, invoice_id
    ):
        invoice_line = self.env["account.invoice.line"]
        invoice_line.create(
            {
                "invoice_id": invoice_id,
                "name": str(freight.name) + " Orden: " + str(origin),
                "product_id": freight.id,
                "price_unit": precio,
                "quantity": 1,
                "account_id": accounts.get("income")
                and accounts["income"].id
                or False,
                "uom_id": freight.uom_id.id,
                "discount": 0,
                "origin": origin,
            }
        )

    def _freight_placement_change(self, freight, placement):
        for rec in self:
            if rec.freigt_placement_status == "invoiced":
                raise ValidationError(
                    _(
                        "You cannot change this values because "
                        "invoice already create for freight "
                        "and placement."
                    )
                )
            else:
                rec.write({"freight": freight, "placement": placement})


class ProductTemplate(models.Model):
    _inherit = "product.product"

    freight = fields.Boolean(string="Freight")
    placement = fields.Boolean(string="Placement")
