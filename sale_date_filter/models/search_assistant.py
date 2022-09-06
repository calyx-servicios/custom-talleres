from odoo import models
from datetime import date


class SearchAssistant(models.TransientModel):
    _inherit = "search.assistant"


    def create_sale_order(self):
        """

        """
        line_obj = self.env['sale.order.line']
        sale_obj = self.env['sale.order']
        lines = []
        must = False

        if self.partner_id:
            for search_wizard in self:
                selection = [
                    line for line in search_wizard.line_ids if line.selected]
                if len(selection) > 0:
                    sale_order = sale_obj.create(
                        {'partner_id': self.partner_id.id,
                            'team_id': self.team_id.id,
                            'date_order_date': date.today(),
                            'warehouse_id': self.warehouse_id.id,
                            'email_partner': self.partner_id.email})
                            
                    for line in search_wizard.line_ids:
                        if line.selected:
                            line_obj.create(self._get_sale_line_values(line.product_id,
                                                                        line.product_uom_qty, sale_order.id,
                                                                        ))
                    return self.action_view_sale_order(sale_order.id)
                    