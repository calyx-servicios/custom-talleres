# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
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

    extra = fields.Boolean(string="Extra Invoice?", default=False)
    freight_extra = fields.Float(
        string="Extra freight",
        track_visibility='onchange'
    )
    placement_extra = fields.Float(
        string="Extra placement",
        track_visibility='onchange'
    )
    extra_freigt_placement_status = fields.Selection(
        [("invoiced", "Invoiced"), ("no", "Nothing in invoice")],
        string="Invoice Status Extra",
        default="no",
    )
    invoice_freight_placement_id_extra = fields.Many2one(
        "account.invoice", string="Invoice Extra"
    )

    @api.multi
    def create_invoice_fregiht_placement(self):
        for rec in self:
            vals = {}
            invoice_obj = self.env["account.invoice"]
            product_obj = self.env["product.product"]
            context = False
            if self._context.get("extra"):
                context = self._context["extra"]

            freight = product_obj.search([("freight", "=", True)], limit=1)
            placement = product_obj.search([("placement", "=", True)], limit=1)
            vals = {
                "partner_id": rec.partner_id.id,
                "team_id": rec.sale_id.team_id.id,
                "origin": rec.name,
                "date_invoice": datetime.datetime.now().date(),
            }

            invoice_id = invoice_obj.create(vals)
            if freight:
                accounts = freight.product_tmpl_id.get_product_accounts()
                if context:
                    rec._create_invoices_lines(
                        accounts,
                        freight,
                        rec.freight_extra,
                        rec.name,
                        invoice_id.id,
                        context,
                    )
                else:
                    rec._create_invoices_lines(
                        accounts,
                        freight,
                        rec.freight,
                        rec.name,
                        invoice_id.id,
                        context,
                    )
            if placement:
                accounts = placement.product_tmpl_id.get_product_accounts()
                if context:
                    rec._create_invoices_lines(
                        accounts,
                        placement,
                        rec.placement_extra,
                        rec.name,
                        invoice_id.id,
                        context,
                    )

                else:
                    rec._create_invoices_lines(
                        accounts,
                        placement,
                        rec.placement,
                        rec.name,
                        invoice_id.id,
                        context,
                    )
            if context:
                rec.extra_freigt_placement_status = "invoiced"
                rec.invoice_freight_placement_id_extra = invoice_id.id
            else:
                rec.freigt_placement_status = "invoiced"
                rec.invoice_freight_placement_id = invoice_id.id

    def _create_invoices_lines(
        self, accounts, freight, precio, origin, invoice_id, context
    ):
        invoice_line = self.env["account.invoice.line"]
        name_line = ""
        if context:
            name_line = str(freight.name) + " Extra - Orden: " + str(origin)
        else:
            name_line = str(freight.name) + " - Orden: " + str(origin)
        invoice_line.create(
            {
                "invoice_id": invoice_id,
                "name": name_line,
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
            view = self.env.ref("sh_message.sh_message_wizard")
            context = dict(self._context or {})
            if rec.freigt_placement_status == "invoiced":
                title = "Warning!"
                context["message"] = (
                    "No puede modificar estos valores porque ya "
                    "existe una factura relacionada para flete y colocación."
                )
                return self.alert_message(title, view, context)
            else:
                rec.write({"freight": freight, "placement": placement})

    def cancel_invoice_fg(self):
        for rec in self:
            invoice = rec.invoice_freight_placement_id
            extra_invoice = rec.invoice_freight_placement_id_extra
            if invoice:
                if invoice.state == "draft":
                    invoice.action_invoice_cancel()
                    rec.freigt_placement_status = "no"
                    rec.invoice_freight_placement_id = False
                    self.env.user.notify_info(
                        "La facturas fue cancelada.", "Información", 1
                    )
                elif invoice.state == ("open" or "cancel"):
                    if invoice.state == "open":
                        self.env.user.notify_warning(
                            "La factura "
                            + str(invoice.display_name)
                            + " no sera cancelada, "
                            "solo se desvinculara de la orden,"
                            " la puede cancelar con una nota de credito.",
                            "Advertencia",
                            1,
                        )
                    rec.freigt_placement_status = "no"
                    rec.invoice_freight_placement_id = False

            if extra_invoice:
                if extra_invoice.state == "draft":
                    extra_invoice.action_invoice_cancel()
                    rec.extra_freigt_placement_status = "no"
                    rec.invoice_freight_placement_id_extra = False
                    rec.extra = False
                    rec.freight_extra = 0
                    rec.placement_extra = 0
                    rec._onchange_fg_extra()
                    self.env.user.notify_info(
                        "La factura extra fue cancelada.", "Información", 1
                    )
                elif extra_invoice.state == ("open" or "cancel"):
                    if extra_invoice.state == "open":
                        self.env.user.notify_warning(
                            "La factura extra "
                            + str(extra_invoice.display_name)
                            + " no sera cancelada, "
                            "solo se desvinculara de la orden"
                            " la puede cancelar con una nota de credito.",
                            "Advertencia",
                            1,
                        )
                    rec.extra_freigt_placement_status = "no"
                    rec.invoice_freight_placement_id_extra = False
                    rec.extra = False
                    rec.freight_extra = 0
                    rec.placement_extra = 0
                    rec._onchange_fg_extra()

    @api.onchange("freight_extra", "placement_extra")
    def _onchange_fg_extra(self):
        for rec in self:
            if rec.sale_id:
                f = rec.freight
                g = rec.placement
                if f and g:
                    f += rec.freight_extra
                    g += rec.placement_extra

    @api.multi
    @api.onchange("extra")
    def onchange_extra(self):
        for rec in self:
            if not rec.extra:
                rec.freight_extra = 0
                rec.placement_extra = 0
                rec._onchange_fg_extra()

    def alert_message(self, title, view, context):
        return {
            "name": title,
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sh.message.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": context,
        }

    @api.multi
    def do_print_picking(self):
        self.write({"printed": True})
        # return self.env.ref('stock.action_report_picking').report_action(self)
        return self.env.ref("stock.action_report_delivery").report_action(self)


class ProductTemplate(models.Model):
    _inherit = "product.product"

    freight = fields.Boolean(string="Freight")
    placement = fields.Boolean(string="Placement")
