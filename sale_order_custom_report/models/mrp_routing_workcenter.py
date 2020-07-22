from odoo import api, models, fields, _
import base64
from odoo.tools.mimetypes import guess_mimetype


class MroRoutingWorkcenter(models.Model):
    _inherit = "mrp.routing.workcenter"

    attachment_ids = fields.Many2many(
        "ir.attachment",
        "routing_workcenter_attachments_rel",
        "workcenter_id",
        "attachment_id",
        string="Attachments",
    )

    blueprint_images = fields.Binary(string="Upload Images", attachment=False)
    blueprint_name = fields.Char(string="BluePrint Name")

    @api.onchange("blueprint_images")
    def _onchange_blueprint_images(self):
        """
            This function adds into the attachment
            the image that the user upload in blueprint_image field
        """
        for record in self:
            if record.blueprint_images:
                mimetype = guess_mimetype(
                    base64.b64decode(record.blueprint_images)
                )
                file_name = record.blueprint_name
                fname = str(file_name.split(".")[1])
                if fname == "jpg" or fname == "jpeg" or fname == "png":
                    new_attach = self.env["ir.attachment"].create(
                        {
                            "name": file_name,
                            "type": "binary",
                            "datas": record.blueprint_images,
                            "mimetype": mimetype,
                            "datas_fname": file_name,
                        }
                    )
                    if new_attach:
                        record.attachment_ids = [(4, new_attach.id)]
                        self.env.user.notify_info(
                            "La imagen fue cargada con éxito.", "Information"
                        )
                        record.blueprint_images = False
                    else:
                        self.env.user.notify_warning(
                            "No se pudo subir el archivo.", "Error"
                        )
                else:
                    self.env.user.notify_warning(
                        "No se pudo subir el archivo.", "Error"
                    )
                    record.blueprint_images = False

