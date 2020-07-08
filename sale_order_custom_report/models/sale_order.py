from odoo import api, models
import base64
from pdf2image import convert_from_path

from io import BytesIO
from datetime import timedelta
import dateutil.parser


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def create_attach_img(self):
        """
            Create a img and attach it in the operation_ids where attach the
            principal blueprints
        """
        for order in self:
            for mrp in order.production_ids:
                for workcenter in mrp.routing_id.operation_ids:
                    if not workcenter.attachment_ids:
                        new_attachment_ids = []
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

    def get_limit_date_produced(self):
        for order in self:
            date = order.date_order
            date = dateutil.parser.parse(date).date()
            new_date = date + timedelta(days=30)
            new_date = new_date.strftime("%d/%m/%Y")
            return new_date
