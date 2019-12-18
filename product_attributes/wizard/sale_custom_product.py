from odoo import models, api, fields, _
from ast import literal_eval
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)

class SaleProductWizardLine(models.TransientModel):
    _name = 'sale.product.wizard.line'
    _description = 'Sale Product Wizard Line'

    wizard_id = fields.Many2one('sale.product.wizard', string='Wizard')
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    attribute_value_id = fields.Many2one('product.attribute.value', string='Attributes')


class SaleProductWizard(models.TransientModel):

    _name = 'sale.product.wizard'
    _description = 'Sale Product Wizard'

    @api.model
    def _default_line_id(self):
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            return line.id

    @api.model
    def _default_note(self):
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            return line.note

    @api.model
    def _default_width(self):
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            return line.width

    @api.model
    def _default_length(self):
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            return line.length

    @api.model
    def _default_height(self):
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            return line.height

    length = fields.Float('Length',default=_default_length)
    height = fields.Float('Height',default=_default_height)
    width = fields.Float('Width',default=_default_width)
    note = fields.Text('Note',default=_default_note)

    @api.model
    def _default_template(self):
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            return line.template_id.id


    @api.model
    def _default_lines(self):
        sale_obj = self.env['sale.order']
        lines = []
        if self._context.get('res_id'):
            line_obj=self.env['sale.order.line']
            line=line_obj.browse(self._context.get('res_id'))
            for attribute in line.product_id.attribute_value_ids:
                lines.append({
                    'attribute_id':attribute.attribute_id.id,
                    'attribute_value_id': attribute.id
                    })

        return lines

    line_ids = fields.One2many('sale.product.wizard.line', 'wizard_id', string='Lines', default=_default_lines)
    template_id = fields.Many2one("product.template", string="Template",default=_default_template, readonly=True)
    line_id = fields.Many2one("sale.order.line", string="Line",default=_default_line_id)

    @api.multi
    def set_product(self):
        product_obj = self.env['product.product']

        for wiz in self:
            domain=[('product_tmpl_id','=',wiz.template_id.id)]

            attribute_vals =[]

            for attribute in wiz.line_ids:
                attribute_vals.append(attribute.attribute_value_id.id)
            product_ids=product_obj.search(domain)
            for product in product_ids:
                check=all(item in attribute_vals for item in product.attribute_value_ids.ids)
                if check:
                    self.line_id.product_id=product.id
                    name = product.name_get()[0][1]
                    if product.description_sale:
                        name += '\n' + product.description_sale
                    message=''
                    if wiz.length>0:
                        message+='Length:'+str(wiz.length)+' '
                    if wiz.width>0:
                        message+='Width:'+str(wiz.width)+' '
                    if wiz.height>0:
                        message+='Height:'+str(wiz.height)+' '
                    if wiz.note:
                        message+=wiz.note
                    if message and len(message)>0:
                        name += '\n Custom:' +message
                    self.line_id.name=name

            self.line_id.length=wiz.length
            self.line_id.height=wiz.height
            self.line_id.width=wiz.width
            self.line_id.note=wiz.note

        return {}
