from odoo import api, models, fields, _
import base64
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)
from PIL import Image
from io import BytesIO
import logging


_logger = logging.getLogger(__name__)


class MroRoutingWorkcenter(models.Model):
    _inherit = "mrp.routing.workcenter"

    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Files",
        help="Get you bank statements in electronic format from your bank and select them here.",
    )


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def print_custom_sale_report(self):
        for order in self:
            for mrp in order.production_ids:
                for workcenter in mrp.routing_id.operation_ids:
                    if not workcenter.attachment_ids:
                        new_attachment_ids = []
                        # for workOrder in mrp.workorder_ids:
                        blueprint = workcenter.worksheet
                        if blueprint:
                            datas = base64.b64decode(blueprint.decode())
                            pdf_file = open("/tmp/pdffile.pdf", "w+b")
                            pdf_file.write(datas)
                            pdf_file.close()
                            images = convert_from_path(
                                "/tmp/pdffile.pdf", fmt="jpeg"
                            )

                            for img in images:
                                buffered = BytesIO()
                                img.save(buffered, format="JPEG")
                                datas = base64.b64encode(buffered.getvalue())

                                iname = workcenter.name + ".jpeg"
                                new_attach = self.env["ir.attachment"].create(
                                    {
                                        "name": iname,
                                        "type": "binary",
                                        "datas": datas,
                                        "mimetype": "jpeg",
                                        "datas_fname": iname,
                                    }
                                )
                                new_attachment_ids.append(new_attach.id)
                            workcenter.write(
                                {
                                    "attachment_ids": [
                                        (6, 0, new_attachment_ids)
                                    ]
                                }
                            )
        return self.env.ref(
            "sale_order_custom_report.action_sale_order_custom_report"
        ).report_action(self)
