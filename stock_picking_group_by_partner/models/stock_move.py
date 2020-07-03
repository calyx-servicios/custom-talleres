import re
from collections import namedtuple
from itertools import groupby
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _assign_picking_post_process(self, new=False):
        res = super(StockMove, self)._assign_picking_post_process(new=new)
        if not new:
            picking = self.mapped("picking_id")
            picking.ensure_one()
            sales = self.mapped("sale_line_id.order_id")
            for sale in sales:
                pattern = r"\b%s\b" % sale.name
                if not re.search(pattern, picking.origin):
                    picking.origin += " " + sale.name
                    picking.message_post_with_view(
                        "mail.message_origin_link",
                        values={"self": picking, "origin": sale},
                        subtype_id=self.env.ref("mail.mt_note").id,
                    )
        return res

    def _assign_picking(self):
            """ Try to assign the moves to an existing picking that has not been
            reserved yet and has the same procurement group, locations and picking
            type (moves should already have them identical). Otherwise, create a new
            picking to assign them to. """
            Picking = self.env['stock.picking']
            grouped_moves = groupby(sorted(self, key=lambda m: [f.id for f in m._key_assign_picking()]), key=lambda m: [m._key_assign_picking()])
            for group, moves in grouped_moves:
                moves = self.env['stock.move'].concat(*list(moves))
                new_picking = False
                # Could pass the arguments contained in group but they are the same
                # for each move that why moves[0] is acceptable
                picking = moves[0]._search_picking_for_assignation()
                if picking:
                    if any(picking.partner_id.id != m.partner_id.id or
                            picking.origin != m.origin for m in moves):
                        # If a picking is found, we'll append `move` to its move list and thus its
                        # `partner_id` and `ref` field will refer to multiple records. In this
                        # case, we chose to  wipe them.
                        picking.with_context(picking_no_overwrite_partner_origin=1).write({
                            'partner_id': False,
                            'origin': False,
                        })
                else:
                    new_picking = True
                    picking = Picking.create(moves._get_new_picking_values())

                moves.write({'picking_id': picking.id})
                moves._assign_picking_post_process(new=new_picking)
            return True


    def _search_picking_for_assignation(self):
        # totally reimplement this one to add a hook to change the domain
        self.ensure_one()
        picking = self.env["stock.picking"].search(
            self._domain_search_picking_for_assignation(), limit=1
        )
        return picking

    def _domain_search_picking_handle_move_type(self):
        """Hook to handle the move type. Can be overloaded by other modules.
        By default the move type is taken from the procurement group.
        """
        # avoid mixing picking policies
        return [("move_type", "=", self.group_id.move_type)]

    def _domain_search_picking_for_assignation(self):
        states = ("draft", "confirmed", "waiting", "partially_available", "assigned")
        if (
            not self.picking_type_id.group_pickings
            or self.group_id.sale_id.picking_policy == "one"
        ):
            # use the normal domain from the stock module
            domain = [
                ("group_id", "=", self.group_id.id),
            ]
        else:
            domain = [
                # same partner
                ("partner_id", "=", self.group_id.partner_id.id),
                # don't search on the procurement.group
            ]
            domain += self._domain_search_picking_handle_move_type()
        domain += [
            ("location_id", "=", self.location_id.id),
            ("location_dest_id", "=", self.location_dest_id.id),
            ("picking_type_id", "=", self.picking_type_id.id),
            ("printed", "=", False),
            ("state", "in", states),
        ]
        if self.env.context.get("picking_no_copy_if_can_group"):
            # we are in the context of the creation of a backorder:
            # don't consider the current move's picking
            domain.append(("id", "!=", self.picking_id.id))
        return domain

    def _key_assign_picking(self):
        return (
            self.sale_line_id.order_id.partner_shipping_id, self.group_id,
            self.location_id, self.location_dest_id, self.picking_type_id,
            PickingPolicy(id=self.sale_line_id.order_id.picking_policy)
        )

# we define a named tuple because the code in module stock expects the values in
# the tuple returned by _key_assign_picking to be records with an id attribute
PickingPolicy = namedtuple("PickingPolicy", ["id"])
