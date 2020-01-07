from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    template_id = fields.Many2one('product.template', string='Product', domain=[('sale_ok', '=', True)])
    length = fields.Float('Length')
    height = fields.Float('Height')
    width = fields.Float('Width')
    note = fields.Text('Note')
    to_quote = fields.Boolean(string='To Quote',help='This means that the price will be set to zero everytime the custom wizard is called')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'sale_line_ir_attachments_rel','wizard_id', 'attachment_id', 'Attachments')
    to_design = fields.Boolean(string='To Design')
    design_ids = fields.Many2many(
        'ir.attachment', 'sale_line_ir_design_attachments_rel','wizard_id', 'attachment_id', 'Design')

    @api.multi
    @api.onchange('length','height','width','note')
    def change_product(self):
        message=''
        if self.length>0:
            message+='Length:'+str(self.length)+'mm '
        if self.width>0:
            message+='Width'+str(self.width)+'mm '
        if self.height>0:
            message+='Width'+str(self.height)+'mm '
        if self.note:
            message+=self.note
        name = self.product_id.name_get()[0][1]
        if self.product_id.description_sale:
            name += '\n' + self.product_id.description_sale
        name += '\n' +message
        self.name=name


    @api.multi
    @api.onchange('price_unit')
    def product_id_change_quote(self):
        if self.price_unit>0.0:
            self.to_quote=False

    @api.multi
    @api.onchange('to_quote')
    def product_id_reset_price(self):
        _logger.debug('===onchange to quote set quote===')
        if self.to_quote:
            self.price_unit=0.0


    @api.multi
    @api.onchange('template_id')
    def change_product(self):
        self.ensure_one()
        product_obj=self.env['product.product']
        _logger.debug('===onchange===')
        attribute_vals=[]
        for attribute in self.template_id.attribute_line_ids:
            for value in attribute.value_ids:
                if value.name.lower() == 'a definir':
                    attribute_vals.append(value.id)

        if attribute_vals and len(attribute_vals)>0:
            _logger.debug('===>%r', attribute_vals)
            product_ids=product_obj.search([('product_tmpl_id','=', self.template_id.id)])
            for product in product_ids:
                check=all(item in attribute_vals for item in product.attribute_value_ids.ids)
                if check:
                    _logger.debug('Product %r in?===>%r' % (attribute_vals,product.attribute_value_ids.ids))
                    self.product_id=product.id
    @api.multi
    def action_custom_selection(self):
        context=self.env.context
        _logger.debug('===>%r', context)
        return {
            'name': _("Product Selector"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.product.wizard',
            'target': 'new',
            }
