from odoo import models, fields, api

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
                                                                        line.product_uom_qty,
                                                                        line.to_quote,
                                                                        line.to_design,
                                                                          sale_order.id,
                                                                        ))
                    return self.action_view_sale_order(sale_order.id)
    
    
    def _get_sale_line_values(self, product_id, quantity, to_quote, to_design, sale_order_id):
        line_obj = self.env['sale.order.line']
        values = {
            'name': product_id.display_name,
            'order_id': sale_order_id,
            'product_id': product_id.id,
            'template_id': product_id.product_tmpl_id.id, #Se agrego campo custom para el cliente Talleres
            'variants_status_ok': True, #Se agrego campo custom para el cliente Talleres
            "to_quote" : to_quote,
            "to_design" :to_design
        }
        values.update(
            line_obj._prepare_add_missing_fields(values))
        values.update(
            {'product_uom_qty': quantity})
        return values
    

class SearchAssistant(models.TransientModel):
    _inherit = "search.assistant.line"


    to_quote = fields.Boolean()
    to_design = fields.Boolean()
    
    @api.multi
    @api.onchange("selected")
    def quote_design_unselection(self):
        if not self.selected:
            self.write({"to_design":False,
                        "to_quote":False,})
                # self.to_design = False
                # self.to_quote = False
