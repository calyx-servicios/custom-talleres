from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    template_id = fields.Many2one(
        "product.template", string="Product", domain=[("sale_ok", "=", True)]
    )
    note = fields.Text("Note")
    to_quote = fields.Boolean(
        string="To Quote",
        help="This means that the price will be set to "
        "zero everytime the custom wizard is called",
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "sale_line_ir_attachments_rel",
        "wizard_id",
        "attachment_id",
        "Attachments",
    )
    to_design = fields.Boolean(string="To Design")
    design_ids = fields.Many2many(
        "ir.attachment",
        "sale_line_ir_design_attachments_rel",
        "wizard_id",
        "attachment_id",
        "Design",
    )
    quote_status = fields.Selection(
        [
            ("to quote", "To Quote"),
            ("quoted", "Quoted"),
            ("no", "Nothing to Quote"),
        ],
        string="Quote Status",
        default="no",
    )
    variants_status_ok = fields.Boolean(string="Variants", default=False)
    product_service = fields.Boolean(string="Product is service", default=False)
   
    @api.multi
    @api.onchange("note")
    def change_product(self):
        message = ""
        if self.note:
            message += self.note
        name = self.product_id.name_get()[0][1]
        if self.product_id.description_sale:
            name += "\n" + self.product_id.description_sale
        name += "\n" + message
        self.name = name

    @api.multi
    @api.onchange("price_unit")
    def product_id_change_quote(self):
        if self.to_quote:
            if self.price_unit > 0.0:
                self.quote_status = "quoted"
                self.to_quote = False

    @api.multi
    @api.onchange("to_quote")
    def product_id_reset_price(self):
        _logger.debug("===onchange to quote set quote===")
        if self.to_quote:
            self.price_unit = 0.0
            self.quote_status = "to quote"
        if not self.to_quote:
            if self.price_unit == 0.0:
                self.price_unit = self.product_id.list_price

    @api.multi
    @api.onchange("to_quote")
    def product_to_quote_associate(self):
        if self.quote_status == "no":
            self.to_design = self.to_quote
        if self.quote_status == "to quote":
            self.to_design = self.to_quote
            self.quote_status = "no"

    @api.multi
    @api.onchange("to_design")
    def product_to_desing_associate(self):
        if self.quote_status == "no":
            self.to_quote = self.to_design
        if self.quote_status == "to quote":
            self.to_quote = self.to_design
            self.quote_status = "no"
        if self.quote_status == "quoted" and self.to_design:
            self.to_quote = self.to_design     

    @api.multi
    @api.onchange("template_id")
    def change_product(self):
        self.ensure_one()
        product_obj = self.env["product.product"]
        _logger.debug("===onchange===")
        attribute_vals = []
        if self.template_id.type == 'service':
            self.product_service = True
        for attribute in self.template_id.attribute_line_ids:
            for value in attribute.value_ids:
                if value.name.lower() == "a definir":
                    attribute_vals.append(value.id)

        if attribute_vals and len(attribute_vals) > 0:
            _logger.debug("===>%r", attribute_vals)
            product_ids = product_obj.search(
                [("product_tmpl_id", "=", self.template_id.id)]
            )
            for product in product_ids:
                check = all(
                    item in attribute_vals
                    for item in product.attribute_value_ids.ids
                )
                if check:
                    _logger.debug(
                        "Product %r in?===>%r"
                        % (attribute_vals, product.attribute_value_ids.ids)
                    )
                    self.product_id = product.id

    @api.multi
    def action_custom_selection(self):
        context = self.env.context
        _logger.debug("===>%r", context)
        return {
            "name": _("Product Selector"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sale.product.wizard",
            "target": "new",
        }

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        if self.quote_status == "no":
            if not self.product_uom or not self.product_id:
                self.price_unit = 0.0
                return
            if self.order_id.pricelist_id and self.order_id.partner_id:
                product = self.product_id.with_context(
                    lang=self.order_id.partner_id.lang,
                    partner=self.order_id.partner_id.id,
                    quantity=self.product_uom_qty,
                    date=self.order_id.date_order,
                    pricelist=self.order_id.pricelist_id.id,
                    uom=self.product_uom.id,
                    fiscal_position=self.env.context.get("fiscal_position"),
                )
                self.price_unit = self.env[
                    "account.tax"
                ]._fix_tax_included_price_company(
                    self._get_display_price(product),
                    product.taxes_id,
                    self.tax_id,
                    self.company_id,
                )

