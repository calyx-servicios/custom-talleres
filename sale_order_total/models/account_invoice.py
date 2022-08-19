from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    sale_ids = fields.Many2one(comodel_name="sale.order")
    sale_id_total = fields.Monetary(compute="_get_total")

    
    @api.multi
    def _get_total(self):
        sales = self.env["sale.order"].search([])
        for record in self:
            total = 0
            for sale in sales:
                if record.origin == sale.name:
                    for sale_line in sale.order_line:
                        total = total + sale_line.price_subtotal
            record.update({"sale_id_total": total})