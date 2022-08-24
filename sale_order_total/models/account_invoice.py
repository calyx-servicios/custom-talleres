from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    sale_order_total = fields.Monetary(compute="_get_total")
    sale_order_untaxed = fields.Monetary(compute="_get_total_untaxed")
    
    @api.multi
    def _get_total_untaxed(self):
        sales = self.env["sale.order"].search([])
        for record in self:
            total = 0
            for sale in sales:
                if sale.state == "sale":
                    if record.origin == sale.name:
                        for sale_line in sale.order_line:
                            total = total + sale_line.price_subtotal
            record.update({"sale_order_untaxed": total})
            

    def _get_total(self):
        sales = self.env["sale.order"].search([])
        for record in self:
            total = 0
            for sale in sales:
                if sale.state == "sale":
                    if record.origin == sale.name:
                        for sale_line in sale.order_line:
                            total = total + sale_line.price_subtotal + record.amount_tax
            record.update({"sale_order_total": total})