from odoo import models, api, fields, _
from ast import literal_eval
from odoo.exceptions import (
    AccessError,
    UserError,
    RedirectWarning,
    ValidationError,
    Warning,
)
import logging

_logger = logging.getLogger(__name__)


class SaleProductWizardLine(models.TransientModel):
    _name = "sale.product.wizard.line"
    _description = "Sale Product Wizard Line"

    wizard_id = fields.Many2one("sale.product.wizard", string="Wizard")
    attribute_id = fields.Many2one("product.attribute", string="Attribute")
    product_ids = fields.Many2many(
        "product.product", string="Variants", readonly=True
    )
    attribute_value_id = fields.Many2one(
        "product.attribute.value", string="Values"
    )


class SaleProductWizardCreate(models.TransientModel):
    _name = "sale.product.wizard.create"
    _description = "Sale Product Attribute Create"

    wizard_id = fields.Many2one("sale.product.wizard", string="Wizard")
    attribute_id = fields.Many2one("product.attribute", string="Attribute")
    product_ids = fields.Many2one(
        "product.template", string="Variants", readonly=True
    )
    attribute_value_id = fields.Many2one(
        "product.attribute.value", string="Values"
    )


class SaleProductWizard(models.TransientModel):

    _name = "sale.product.wizard"
    _description = "Sale Product Wizard"

    @api.model
    def _default_line_id(self):
        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))
            return line.id

    @api.model
    def _default_note(self):
        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))
            return line.note

    # @api.model
    # def _default_width(self):
    #     if self._context.get("res_id"):
    #         line_obj = self.env["sale.order.line"]
    #         line = line_obj.browse(self._context.get("res_id"))
    #         return line.width

    # @api.model
    # def _default_length(self):
    #     if self._context.get("res_id"):
    #         line_obj = self.env["sale.order.line"]
    #         line = line_obj.browse(self._context.get("res_id"))
    #         return line.length

    # @api.model
    # def _default_height(self):
    #     if self._context.get("res_id"):
    #         line_obj = self.env["sale.order.line"]
    #         line = line_obj.browse(self._context.get("res_id"))
    #         return line.height

    @api.model
    def _default_to_quote(self):
        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))
            return line.to_quote

    # length = fields.Float("Length (Cm)", default=_default_length)
    # height = fields.Float("Height (Cm)", default=_default_height)
    # width = fields.Float("Width (Cm)", default=_default_width)
    note = fields.Text("Note", default=_default_note)

    @api.model
    def _default_template(self):
        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))
            return line.template_id.id

    @api.model
    def _default_lines(self):
        product_obj = self.env["product.product"]
        lines = []
        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))
            domain = [("product_tmpl_id", "=", line.template_id.id)]
            product_ids = product_obj.search(domain).ids
            for attribute in line.product_id.attribute_value_ids:
                lines.append(
                    {
                        "attribute_id": attribute.attribute_id.id,
                        "product_ids": product_ids,
                        "attribute_value_id": attribute.id,
                    }
                )

        return lines

    @api.model
    def _default_attachments(self):
        # sale_obj = self.env["sale.order"]
        # product_obj = self.env["product.product"]
        lines = []

        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))

            for attribute in line.attachment_ids:
                lines.append(attribute.id)

        return lines

    @api.model
    def _default_design_attachments(self):
        # sale_obj = self.env["sale.order"]
        # product_obj = self.env["product.product"]
        lines = []

        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))

            for attribute in line.design_ids:
                lines.append(attribute.id)

        return lines

    @api.model
    def _default_to_design(self):
        if self._context.get("res_id"):
            line_obj = self.env["sale.order.line"]
            line = line_obj.browse(self._context.get("res_id"))
            return line.to_design

    @api.model
    def _default_design_view(self):
        if self._context.get("design"):
            return True
        else:
            return False

    line_ids = fields.One2many(
        "sale.product.wizard.line",
        "wizard_id",
        string="Lines",
        default=_default_lines,
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "product_custom_ir_attachments_rel",
        "wizard_id",
        "attachment_id",
        "Attachments",
        default=_default_attachments,
    )
    design_ids = fields.Many2many(
        "ir.attachment",
        "product_custom_ir_design_attachments_rel",
        "wizard_id",
        "attachment_id",
        "Design Attachments",
        default=_default_design_attachments,
    )
    template_id = fields.Many2one(
        "product.template",
        string="Template",
        default=_default_template,
        readonly=True,
    )
    line_id = fields.Many2one(
        "sale.order.line", string="Line", default=_default_line_id
    )
    to_design = fields.Boolean(string="To Design", default=_default_to_design)

    line_create_ids = fields.One2many(
        "sale.product.wizard.create", "wizard_id", string="Lines",
    )

    design_view = fields.Boolean(
        string="Design View", default=_default_design_view
    )

    @api.multi
    def set_product(self):
        product_obj = self.env["product.product"]
        for wiz in self:
            domain = [("product_tmpl_id", "=", wiz.template_id.id)]

            attribute_vals = []

            for attribute in wiz.line_ids:
                attribute_vals.append(attribute.attribute_value_id.id)
            product_ids = product_obj.search(domain)
            for product in product_ids:
                check = all(
                    item in attribute_vals
                    for item in product.attribute_value_ids.ids
                )
                if check:
                    self.line_id.product_id = product.id
                    self.line_id.price_unit = product.lst_price
                    name = product.name_get()[0][1]
                    if product.description_sale:
                        name += "\n" + product.description_sale
                    message = ""
                    # if wiz.length > 0:
                    #     message += "Length:" + str(wiz.length) + " "
                    # if wiz.width > 0:
                    #     message += "Width:" + str(wiz.width) + " "
                    # if wiz.height > 0:
                    #     message += "Height:" + str(wiz.height) + " "
                    if wiz.note:
                        message += wiz.note
                    if message and len(message) > 0:
                        name += "\n Custom:" + message
                    self.line_id.name = name

            # self.line_id.length = wiz.length
            # self.line_id.height = wiz.height
            # self.line_id.width = wiz.width
            self.line_id.note = wiz.note
            # if wiz.attachment_ids:
            #     new_attachment_ids = []

            #     for attachment in wiz.attachment_ids:
            #         new_attachment_ids.append(attachment.id)
            #     self.line_id.write(
            #         {"attachment_ids": [(6, 0, new_attachment_ids)]}
            #     )
            # else:
            #     self.line_id.write({"attachment_ids": [(6, 0, [])]})
            if wiz.design_ids:
                new_attachment_ids = []

                for attachment in wiz.design_ids:
                    new_attachment_ids.append(attachment.id)
                self.line_id.write(
                    {"design_ids": [(6, 0, new_attachment_ids)]}
                )
            else:
                self.line_id.write({"design_ids": [(6, 0, [])]})

        return {}

    @api.multi
    def set_new_variant(self):
        attribute_line = self.env["product.attribute.line"]
        for wiz in self:
            product_obj = wiz.template_id
            domain = [("product_tmpl_id", "=", product_obj.id)]
            attribute_line_ids = attribute_line.search(domain)

            for rec in wiz.line_create_ids:
                attribute = attribute_line_ids.filtered(
                    lambda x: x.attribute_id == rec.attribute_id
                )
                rec.attribute_value_id.update({"create_from_sale": True})

                if attribute:
                    for line in attribute:
                        if rec.attribute_value_id not in line.value_ids:
                            line.write(
                                {"value_ids": [(4, rec.attribute_value_id.id)]}
                            )
                            product_obj.create_variant_ids()

                else:
                    # attribute_value = self.env["product.attribute.value"]
                    # domain_att = [("attribute_id", "=", rec.attribute_id.id)]
                    # attribute_vals = []
                    # values = attribute_value.search(domain_att)

                    # for value in values:
                    #     if value.name.lower() == ("a definir" or "nulo"):
                    #         attribute_vals.append(value.id)

                    # if not attribute_vals and len(attribute_vals) == 0:
                    #     vals = {
                    #         "name": "Nulo",
                    #         "attribute_id": rec.attribute_id.id,
                    #         "sequence": 10,
                    #     }
                    #     attribute_value.create(vals)

                    product_obj.write(
                        {
                            "attribute_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "attribute_id": rec.attribute_id.id,
                                        "value_ids": [
                                            (4, rec.attribute_value_id.id),
                                            # (4, attribute_value.id),
                                        ],
                                    },
                                )
                            ]
                        }
                    )
                # product_obj.create_variant_ids()

        return {
            "name": _("Product Selector"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sale.product.wizard",
            "target": "new",
        }
