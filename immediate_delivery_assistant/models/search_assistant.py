from odoo import models, api


class SearchAssistant(models.TransientModel):

    _inherit = "search.assistant"

    def _search(self, selected_products=None):
        print("ALMACEN", self.warehouse_id.name)
        product_obj = self.env['product.product']
        self.line_ids = False
        domain = self._get_domain_filter()
        if len(domain) > 0:
            product_ids = product_obj.search(domain)
            line_ids = []
            for product in product_ids:
                selected = self.selected
                if self.warehouse_id.name=="Taller" and product.immediate_delivery:
                    continue
                if not self.selected and selected_products:
                    selected = selected_products and product.id in selected_products
                
                available_qty = self.env['stock.quant']._get_available_quantity(product, self.warehouse_id.view_location_id)
                line_ids.append((0, 0, {
                    'selected': selected,
                    'product_id': product.id,
                    'attribute_value_ids': [(6, 0, product.attribute_value_ids.ids)],
                    'price_unit': product.list_price,
                    'qty_available_today': available_qty,
                    'description': product.description or '',
                    'brand_id': product.product_tmpl_id.product_brand_id
                }))

            self.line_ids = line_ids


