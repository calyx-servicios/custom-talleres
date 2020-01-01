# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"


    design_status = fields.Selection([
            ('to design', 'To Design'),
            ('in design', 'In Design'),
            ('ready', 'Ready'),
            ('no', 'Nothing to Design')
            ], string='Design Status', default='no',track_visibility='onchange')

    production_ids = fields.Many2many("mrp.production", string='Productions', compute="_get_produced", readonly=True, copy=False)
    production_count = fields.Integer(string='# of Productions', compute='_get_produced', readonly=True)
    production_status = fields.Selection([
            ('to produce', 'To Produce'),
            ('in production', 'En Produccion'),
            ('ready', 'Ready'),
            ('no', 'Nothing to Produce')
            ], string='Production Status', compute='_get_produced_state', store=True, readonly=True)

    @api.depends('production_ids','production_ids.state')
    def _get_produced_state(self):
        _logger.debug('======debug===== get produced')
        for order in self:
            line_production_status=[]
            for prod in order.production_ids:
                line_production_status.append(prod.state)
            _logger.debug('======production> %r', line_production_status)
            production_count=len(line_production_status)
            production_status = 'no'
            if production_count>0:
                if order.state not in ('sale', 'done'):
                    production_status = 'no'
                elif any(production_status in ['confirmed'] for production_status in line_production_status):
                    production_status = 'to produce'
                elif all(production_status in ['progress'] for production_status in line_production_status):
                    production_status = 'in production'
                elif all(production_status in ['done'] for production_status in line_production_status):
                    production_status = 'ready'
                else:
                    production_status = 'no'
            order.update({
                'production_status': production_status
            })

    @api.depends('state')
    def _get_produced(self):
        _logger.debug('======debug===== get produced')
        for order in self:
            production_obj=self.env['mrp.production']
            production_ids=production_obj.search([('sale_id','=',order.id)])
            line_production_status=[]
            for prod in production_ids:
                line_production_status.append(prod.state)
            _logger.debug('======production> %r', line_production_status)
            production_count=len(line_production_status)
            production_status = 'no'
            if production_count>0:
                if order.state not in ('sale', 'done'):
                    production_status = 'no'
                elif all(production_status in ['confirmed'] for production_status in line_production_status):
                    production_status = 'to produce'
                elif any(production_status in ['progress'] for production_status in line_production_status):
                    production_status = 'in production'
                elif all(production_status in ['done'] for production_status in line_production_status):
                    production_status = 'ready'
                else:
                    production_status = 'no'



            _logger.debug('=====order data %r %r %r=====' % (production_ids, production_status, production_count))
            order.update({
                'production_ids': production_ids.ids or False,
                'production_status': production_status,
                'production_count': production_count
            })


    @api.multi
    def action_view_productions(self):
        productions = self.mapped('production_ids')
        action = self.env.ref('sale_order_workflow.mrp_production_sale_action').read()
        _logger.debug('=====view production? %r ' % action)
        action = {
                'name': _('Productions'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'mrp.production',
                'view_id': False, #self.env.ref('mrp.mrp_production_tree_view').id,
                'type': 'ir.actions.act_window',
                'domain': None,
                'res_id': None
                }

        if len(productions) > 1:
            action['domain'] = [('id', 'in', productions.ids)]
        elif len(productions) == 1:
            action['view_id'] = self.env.ref('mrp.mrp_production_form_view').id
            action['res_id'] = productions.ids[0]
            action['view_mode']= 'form'
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_confirm(self):
        res=super(SaleOrder, self).action_confirm()
        production_obj=self.env['mrp.production']
        if res:
            for order in self:
                for line in order.order_line:
                    production_ids=production_obj.search([('sale_id','=',order.id),('product_id','=',line.product_id.id)])
                    if line.attachment_ids:
                        new_attachment_ids=[]
                        for attach in line.attachment_ids:
                            new_attachment_ids.append(attach.id)
                        for prod in production_ids:
                            prod.write({'attachment_ids': [(6, 0, new_attachment_ids)]})
                    else:
                        if line.template_id:
                            if line.template_id.attachment_ids:
                                new_attachment_ids=[]
                                for attach in line.template_id.attachment_ids:
                                    new_attachment_ids.append(attach.id)
                                for prod in production_ids:
                                    prod.write({'attachment_ids': [(6, 0, new_attachment_ids)]})

            return True
