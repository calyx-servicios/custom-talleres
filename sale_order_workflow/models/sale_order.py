# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
import datetime
import dateutil.parser
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("to design", "To Design"),
            ("sent design", "Quotation Design"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        readonly=True,
        copy=False,
        index=True,
        tracking=3,
        default="draft",
    )

    design_status = fields.Selection(
        [
            ("to design", "To Design"),
            ("in design", "In Design"),
            ("ready", "Designed"),
            ("no", "Nothing to Design"),
        ],
        string="Design Status",
        default="no",
        # compute="_get_design",
        track_visibility="onchange",
    )
    quote_status = fields.Selection(
        [
            ("to quote", "To Quote"),
            ("quoted", "Quoted"),
            ("no", "Nothing to Quote"),
        ],
        string="Quote Status",
        default="no",
        compute="_get_quote_state",
        track_visibility="onchange",
    )

    production_ids = fields.Many2many(
        "mrp.production",
        string="Productions",
        compute="_get_produced",
        readonly=True,
        copy=False,
    )
    production_count = fields.Integer(
        string="# of Productions", compute="_get_produced", readonly=True,
    )
    production_status = fields.Selection(
        [
            ("to produce", "To Produce"),
            ("in production", "In Production"),
            ("ready", "Produced"),
            ("no", "Nothing to Produce"),
        ],
        string="Production Status",
        compute="_get_produced_state",
        # store=True,
        readonly=True,
    )
    picking_status = fields.Selection(
        [
            ("no", "Nothing to Deliver"),
            ("draft", "New"),
            ("cancel", "Cancelled"),
            ("waiting", "Waiting Another Move"),
            ("confirmed", "Waiting Availability"),
            ("partially_available", "Partially Available"),
            ("assigned", "Available"),
            ("done", "Done"),
        ],
        string="Picking Status",
        compute="_get_picking_state",
        # store=True,
        readonly=True,
    )
    design_ids = fields.Many2many(
        "ir.attachment",
        "sale_line_ir_design_rel",
        "wizard_id",
        "attachment_id",
        "Design Attachments",
    )

    final_countdown = fields.Char(
        string="Production Countdown Days", compute="production_countdown",
    )

    date_produced_state = fields.Date(
        string="Produced Date Done", compute="date_done_production"
    )

    freight = fields.Float(string="Freight")

    placement = fields.Float(string="Placement")

    freight_defined = fields.Boolean(string="Freight Defined?")

    placement_defined = fields.Boolean(string="Placement Defined?")

    @api.depends("state", "production_ids", "production_ids.state")
    def _get_produced_state(self):
        # _logger.debug("======debug===== get produced")
        for order in self:
            line_production_status = []
            for prod in order.production_ids:
                line_production_status.append(prod.state)
            production_count = len(line_production_status)
            production_status = "no"
            if production_count > 0:
                if order.state not in ("sale", "done"):
                    production_status = "no"
                elif any(
                    production_status in ["confirmed", "planned"]
                    for production_status in line_production_status
                ):
                    production_status = "to produce"
                    # _logger.info(
                    #     "======product1ion> %r", line_production_status
                    # )
                elif all(
                    production_status in ["progress"]
                    for production_status in line_production_status
                ):
                    production_status = "in production"
                elif all(
                    production_status in ["done"]
                    for production_status in line_production_status
                ):
                    production_status = "ready"
                # else:
                #     production_status = "no"
            order.update({"production_status": production_status})

    @api.depends("state", "picking_ids", "picking_ids.state")
    def _get_picking_state(self):
        _logger.debug("======debug===== get pickings")
        for order in self:
            line_picking_status = []
            for pick in order.picking_ids:
                line_picking_status.append(pick.state)
            _logger.debug("======pickings> %r", line_picking_status)
            picking_count = len(line_picking_status)
            picking_status = "no"
            if picking_count > 0:
                if order.state not in ("sale", "done"):
                    picking_status = "no"
                elif any(
                    picking_status in ["confirmed", ["waiting"]]
                    for picking_status in line_picking_status
                ):
                    picking_status = "confirmed"
                elif all(
                    picking_status in ["partially_available", "assigned"]
                    for picking_status in line_picking_status
                ):
                    picking_status = "assigned"
                elif all(
                    picking_status in ["done"]
                    for picking_status in line_picking_status
                ):
                    picking_status = "done"
                else:
                    picking_status = "no"
            order.update({"picking_status": picking_status})

    @api.depends("state")
    def _get_produced(self):
        # _logger.debug("======debug===== get produced")
        for order in self:
            production_obj = self.env["mrp.production"]
            production_ids = production_obj.search(
                [("sale_id", "=", order.id)]
            )
            line_production_status = []
            for prod in production_ids:
                line_production_status.append(prod.state)
            # _logger.info("======production> %r", line_production_status)
            production_count = len(line_production_status)
            production_status = "no"
            if production_count > 0:
                if order.state not in ("sale", "done"):
                    production_status = "no"
                elif all(
                    production_status in ["confirmed"]
                    for production_status in line_production_status
                ):
                    production_status = "to produce"
                elif any(
                    production_status in ["progress"]
                    for production_status in line_production_status
                ):
                    production_status = "in production"
                elif all(
                    production_status in ["done"]
                    for production_status in line_production_status
                ):
                    production_status = "ready"
                else:
                    production_status = "no"

            # _logger.debug(
            #     "=====order data %r %r %r====="
            #     % (production_ids, production_status, production_count)
            # )
            order.update(
                {
                    "production_ids": production_ids.ids or False,
                    # "production_status": production_status,
                    "production_count": production_count,
                }
            )

    @api.depends("order_line.quote_status")
    def _get_quote_state(self):
        for order in self:
            line_quote_status = []
            for line in order.order_line:
                line_quote_status.append(line.quote_status)
            quote_state = "no"
            quote_count = len(line_quote_status)
            if quote_count > 0:
                if any(q_s in ["to quote"] for q_s in line_quote_status):
                    quote_state = "to quote"
                elif all(q_s in ["quoted"] for q_s in line_quote_status):
                    quote_state = "quoted"
                elif any(
                    q_s in ["quoted"] for q_s in line_quote_status
                ) and all(
                    q_s not in ["to quote"] for q_s in line_quote_status
                ):
                    quote_state = "quoted"
                elif all(q_s in ["no"] for q_s in line_quote_status):
                    quote_state = "no"
            order.update({"quote_status": quote_state})

    @api.multi
    def action_confirm_new(self):
        for order in self:
            if order.state != "sent design":
                for line in order.order_line:
                    if line.to_design:
                        raise ValidationError(
                            _(
                                "You cannot confirm sales with"
                                " products to design."
                            )
                        )
                order.action_confirm()
            else:
                order.action_confirm()

    @api.multi
    def action_view_productions(self):
        productions = self.mapped("production_ids")
        action = self.env.ref(
            "sale_order_workflow.mrp_production_sale_action"
        ).read()
        _logger.debug("=====view production? %r " % action)
        action = {
            "name": _("Productions"),
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "mrp.production",
            "view_id": False,
            "type": "ir.actions.act_window",
            "domain": None,
            "res_id": None,
        }

        if len(productions) > 1:
            action["domain"] = [("id", "in", productions.ids)]
        elif len(productions) == 1:
            action["view_id"] = self.env.ref("mrp.mrp_production_form_view").id
            action["res_id"] = productions.ids[0]
            action["view_mode"] = "form"
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # production_obj = self.env["mrp.production"]
        if res:
            for order in self:
                if order.quote_status not in ["no", "quoted"]:
                    raise ValidationError(
                        _(
                            "You cannot confirm sales with quote task "
                            "in progress."
                        )
                    )

                for pick in order.picking_ids:
                    f = 0
                    g = 0
                    if order.freight_defined:
                        f = order.freight
                    if order.placement_defined:
                        g = order.placement
                    pick.write({"freight": f, "placement": g})

                for line in order.order_line:
                    if line.route_id:
                        for procurement in line.route_id.pull_ids:
                            if procurement.procure_method in [
                                "make_to_order"
                            ] and not (
                                order.warehouse_id.manufacture_to_resupply
                            ):
                                raise ValidationError(
                                    _(
                                        "You cannot confirm sales with "
                                        "make_to_order procurement "
                                        "rules on this warehouse."
                                    )
                                )
                            if procurement.procure_method in [
                                "make_to_stock"
                            ] and (line.to_quote or line.to_design):
                                raise ValidationError(
                                    _(
                                        "You cannot confirm sales with "
                                        "make_to_stock procurement "
                                        "rules for custom products."
                                    )
                                )

                # for line in order.order_line:
                #     production_ids = production_obj.search(
                #         [
                #             ("sale_id", "=", order.id),
                #             ("product_id", "=", line.product_id.id),
                #         ]
                #     )
                #     if line.design_ids:
                #         new_attachment_ids = []
                #         for attach in line.design_ids:
                #             new_attachment_ids.append(attach.id)
                #         for prod in production_ids:
                #             prod.write(
                #                 {
                #                     "attachment_ids": [
                #                         (6, 0, new_attachment_ids)
                #                     ]
                #                 }
                #             )
                #     else:
                #         if line.template_id:
                #             if line.template_id.attachment_ids:
                #                 new_attachment_ids = []
                #                 for attach in line.template_id.attachment_ids:
                #                     new_attachment_ids.append(attach.id)
                #                 for prod in production_ids:
                #                     prod.write(
                #                         {
                #                             "attachment_ids": [
                #                                 (6, 0, new_attachment_ids,)
                #                             ]
                #                         }
                #                     )

            return res

    @api.multi
    def _get_production_route(self):
        Pull = self.env["stock.location.route"]
        res = Pull.search(
            expression.AND([[("sale_selectable", "=", True)]]),
            order="sequence desc",
            limit=1,
        )
        _logger.debug("=====production rute___%r" % res.name)
        return res

    @api.multi
    @api.onchange(
        "state", "order_line", "order_line.to_design", "order_line.to_quote",
    )
    def line_design_change(self):
        route_id = self._get_production_route()

        for order in self:
            quote_status = order.quote_status
            for line in order.order_line:

                if line.to_quote:
                    quote_status = "to quote"

                if line.to_quote or line.to_design:
                    line.update({"route_id": route_id})
            order.update({"quote_status": quote_status})

    @api.multi
    def production_countdown(self):
        for rec in self:
            days_default = 30
            actual_date = datetime.datetime.now().date()
            if (
                rec.production_status == "to produce"
                or rec.production_status == "in production"
            ):
                date_confirmation = dateutil.parser.parse(
                    rec.confirmation_date
                ).date()
                days_countdown = actual_date - date_confirmation
                days_countdown = days_countdown.days
                production_countdown_days = days_default - days_countdown
                rec.update({"final_countdown": production_countdown_days})
            if rec.production_status == "ready":
                date_confirmation = dateutil.parser.parse(
                    rec.confirmation_date
                ).date()
                if rec.date_produced_state:
                    date_done = dateutil.parser.parse(
                        rec.date_produced_state
                    ).date()
                    days_countdown = date_done - date_confirmation
                    days_countdown = days_countdown.days
                    production_countdown_days_stop = (
                        days_default - days_countdown
                    )
                    rec.update(
                        {"final_countdown": production_countdown_days_stop}
                    )

    @api.depends("production_status")
    def date_done_production(self):
        for rec in self:
            date_produced_state = ""
            if rec.production_status == "ready":
                for prod in rec.production_ids:
                    date_produced_state = dateutil.parser.parse(
                        prod.date_finished
                    ).date()
                rec.update({"date_produced_state": date_produced_state})

    @api.multi
    @api.onchange("warehouse_id", "order_line")
    def _onchange_warehouse(self):
        for rec in self:
            Pull = self.env["stock.location.route"]
            res = Pull.search(
                [
                    ("sale_selectable", "=", True),
                    ("warehouse_ids", "in", (rec.warehouse_id.ids),),
                ],
                order="sequence",
                limit=1,
            )
            for line in rec.order_line:
                line.route_id = res.id

    @api.multi
    @api.onchange("freight", "placement")
    def _onchange_freight_placement(self):
        for rec in self:
            freight = rec.freight
            placement = rec.placement
            for pick in rec.picking_ids:
                pick._freight_placement_change(freight, placement)

    @api.multi
    @api.onchange("freight_defined")
    def _onchange_freight_defined(self):
        for rec in self:
            if not rec.freight_defined:
                rec.write({"freight": 0})

    @api.multi
    @api.onchange("placement_defined")
    def _onchange_placement_defined(self):
        for rec in self:
            if not rec.placement_defined:
                rec.write({"placement": 0})

    def action_to_design(self):
        for rec in self:
            design_cont = 0
            if not rec.order_line:
                raise ValidationError(
                    _("You cannot design sales without products.")
                )

            for line in rec.order_line:
                if line.to_design:
                    design_cont += 1

            if rec.quote_status != "quoted":
                raise ValidationError(
                    _("You cannot change sales without quoted.")
                )
            if design_cont == 0:
                raise ValidationError(
                    _("You cannot change sales without products to design.")
                )
            else:
                for line in rec.order_line:
                    if line.to_design:
                        product_obj = line.template_id
                        for attribute in product_obj.attribute_line_ids:
                            for value in attribute.value_ids:
                                if value.create_from_sale:
                                    attribute.write(
                                        {"value_ids": [(3, value.id)]}
                                    )
                                    product_obj.create_variant_ids()

                return self.write({"state": "to design"})

    def action_sent_design(self):
        for order in self:
            for line in order.order_line:
                if line.to_design:
                    mrp_obj = self.env["mrp.bom"]
                    domain = [
                        ("product_tmpl_id", "=", line.template_id.id),
                        ("product_id", "=", line.product_id.id),
                    ]
                    bom_s = mrp_obj.search(domain, limit=1)
                    if not bom_s:
                        raise ValidationError(
                            _(
                                "You cannot sent to design because the product "
                                "%s don't have BOM." % (line.template_id.name)
                            )
                        )
            return order.write({"state": "sent design"})


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _get_route(self):
        Pull = self.env["stock.location.route"]
        res = Pull.search(
            expression.AND([[("sale_selectable", "=", True)]]),
            order="sequence",
            limit=1,
        )
        return res

    route_id = fields.Many2one(
        "stock.location.route",
        string="Route",
        domain=[("sale_selectable", "=", True)],
        ondelete="restrict",
        # default=_get_route,
    )

    @api.multi
    def create_new_design(self):
        view_id = self.env.ref("mrp.mrp_bom_form_view").id
        view_tree = self.env.ref("mrp.mrp_bom_tree_view").id
        mrp_obj = self.env["mrp.bom"]
        boms = []
        domain = [
            ("product_tmpl_id", "=", self.template_id.id),
            ("product_id", "=", self.product_id.id),
        ]
        bom_s = mrp_obj.search(domain, limit=1)
        if not bom_s:
            domain = [
                ("product_tmpl_id", "=", self.template_id.id),
                ("product_id", "=", False),
            ]
            bom = mrp_obj.search(domain, limit=1)
            return {
                "name": "Lista de Materiales",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "mrp.bom",
                "view_id": view_id,
                "target": "current",
                "type": "ir.actions.act_window",
                "context": {
                    "default_product_tmpl_id": self.template_id.id,
                    "default_product_id": self.product_id.id,
                    # "default_bom_line_ids": bom.bom_line_ids.ids,
                    "default_bom_line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": x.product_id.id,
                                "product_uom_id": x.product_id.uom_id.id,
                                "product_qty": x.product_qty,
                            },
                        )
                        for x in bom.bom_line_ids
                    ],
                    "default_design": True,
                },
            }
        else:
            for b in bom_s:
                boms.append(b.id)
            return {
                "type": "ir.actions.act_window",
                "name": "New Design BOM",
                "views": [[view_tree, "tree"], [view_id, "form"]],
                "res_model": "mrp.bom",
                "domain": [("id", "in", boms)],
                "target": "current",
            }


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    create_from_sale = fields.Boolean(
        string="Create from sale?", default=False
    )


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    design = fields.Boolean("Design?", default=False)

    @api.model
    def create(self, values):
        bom = super(MrpBom, self).create(values)
        if bom.design:
            if not bom.routing_id:
                raise ValidationError(
                    _("You can't save design bom without routing")
                )
        return bom
