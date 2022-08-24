from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"


    design = fields.Boolean(compute="_get_design", store=True)


    @api.depends("sale_id.order_line.to_design")
    def _get_design(self):
        for record in self:
            for product in record.sale_id.order_line:
                if product.to_design == True:
                    record.update({"design": True})
                else:
                    record.update({"design": False})
                    