from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    sale_order_zone_ids = fields.Many2one("sale.order.zone", string="Zone")


    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , s.zone_ids as sale_order_zone_ids
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.zone_ids"
        return group_by_str



    # def _select(self):
    #     select_str = """
    #         WITH currency_rate as (%s)
    #         SELECT min(l.id) as id,
    #                 l.product_id as product_id,
    #                 t.uom_id as product_uom,
    #                 sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
    #                 sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
    #                 sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
    #                 sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
    #                 sum(l.price_total / COALESCE(NULLIF(cr.rate, 0), 1.0)) as price_total,
    #                 sum(l.price_subtotal / COALESCE(NULLIF(cr.rate, 0), 1.0)) as price_subtotal,
    #                 sum(l.amt_to_invoice / COALESCE(NULLIF(cr.rate, 0), 1.0)) as amt_to_invoice,
    #                 sum(l.amt_invoiced / COALESCE(NULLIF(cr.rate, 0), 1.0)) as amt_invoiced,
    #                 count(*) as nbr,
    #                 s.name as name,
    #                 s.date_order as date,
    #                 s.confirmation_date as confirmation_date,
    #                 s.state as state,
    #                 s.partner_id as partner_id,
    #                 s.user_id as user_id,
    #                 s.company_id as company_id,
    #                 sz.name as sale_order_zone,
    #                 extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
    #                 t.categ_id as categ_id,
    #                 s.pricelist_id as pricelist_id,
    #                 s.analytic_account_id as analytic_account_id,
    #                 s.team_id as team_id,
    #                 p.product_tmpl_id,
    #                 partner.country_id as country_id,
    #                 partner.commercial_partner_id as commercial_partner_id,
    #                 sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
    #                 sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume
    #     """ % self.env['res.currency']._select_companies_rates()
    #     return select_str

    # def _group_by(self):
    #     group_by_str = """
    #         GROUP BY l.product_id,
    #                 l.order_id,
    #                 t.uom_id,
    #                 t.categ_id,
    #                 s.name,
    #                 s.date_order,
    #                 s.confirmation_date,
    #                 s.partner_id,
    #                 s.user_id,
    #                 s.state,
    #                 s.company_id,
    #                 s.pricelist_id,
    #                 s.analytic_account_id,
    #                 s.team_id,
    #                 sz.name,
    #                 p.product_tmpl_id,
    #                 partner.country_id,
    #                 partner.commercial_partner_id
    #     """
    #     return group_by_str

    # def _from(self):
    #     from_str = """
    #       sale_order_line l
    #     join sale_order s on (l.order_id=s.id)
    #     join sale_order_zone sz on (s.zone_name_name = sz.name)
    #     join res_partner partner on s.partner_id = partner.id
    #         left join product_product p on (l.product_id=p.id)
    #             left join product_template t on (p.product_tmpl_id=t.id)
    #     left join product_uom u on (u.id=l.product_uom)
    #     left join product_uom u2 on (u2.id=t.uom_id)
    #     left join product_pricelist pp on (s.pricelist_id = pp.id)
    #     left join currency_rate cr on (cr.currency_id = pp.currency_id and
    #         cr.company_id = s.company_id and
    #         cr.date_start <= coalesce(s.date_order, now()) and
    #         (cr.date_end is null or cr.date_end > coalesce(s.date_order, now())))   
    #     """
    #     return from_str

    # @api.multi
    # def _get_zone(self):
    #     for sale in sales:
    #         for record in self:
    #             if sale.sale_id:
    #                 record.update({"sale_order_zone": sale.zone_name})
    #             else:
    #                 record.update({"sale_order_zone": False})
            