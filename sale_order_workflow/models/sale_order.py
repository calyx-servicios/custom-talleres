# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('design', 'Design'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

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
                elif any(production_status in ['confirmed'] for production_status in line_production_status):
                    production_status = 'to produce'
                elif all(production_status in ['progress'] for production_status in line_production_status):
                    production_status = 'in production'
                elif all(production_status in ['done'] for production_status in line_production_status):
                    production_status = 'ready'
                else:
                    production_status = 'no'



            _logger.debug('=====order data %r %r %r=====' % (production_ids, production_status, production_count))
            order.update({
                'production_ids': production_ids.ids or False,
                'production_count': production_count
            })

    @api.multi
    def action_design(self):
        return self.write({'state': 'design'})

    @api.multi
    def action_view_productions(self):
        productions = self.mapped('production_ids')
        action = self.env.ref('sale_order_workflow.mrp_production_sale_action').read()
        _logger.debug('=====view production? %r ' % action)
        action = {
                'name': _('Productions'),
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'mrp.production',
                'view_id': self.env.ref('mrp.mrp_production_tree_view').id,
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
