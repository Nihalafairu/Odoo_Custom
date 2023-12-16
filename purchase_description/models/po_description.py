from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons.stock.models.stock_rule import ProcurementException
from odoo.tools import groupby


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, company_id, values,
                                                      po, sale_ref):


        res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, company_id,
                                                                    values, po)
        print(res)

        # print(product_id,"pr")
        purchase_order = self.env['purchase.order'].browse(res['order_id'])
        # print(purchase_order.order_line)
        sale_order = self.env['sale.order'].search([('name', '=', sale_ref)])
        print('jjj', sale_order)
        order_line = sale_order.order_line.filtered(lambda l: l.product_id.id == product_id.id)
        print(res['move_dest_ids'][0][1])

        for line in order_line:
            stock_id=self.env['stock.move'].browse(int(res['move_dest_ids'][0][1]))
            if line.id == stock_id.sale_line_id.id:
                res['name'] = line.name


          # if res['product_id']==product_id.id:
                # print(record)
                # print(record.product_id)
                #


            #
            # print(line, "pppppp")
            #
            # print(p, "ppppppppppppppppppppppppppppp")
        return res


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_buy(self, procurements):
        procurements_by_po_domain = defaultdict(list)
        errors = []
        for procurement, rule in procurements:
            # Get the schedule date in order to find a valid seller
            procurement_date_planned = fields.Datetime.from_string(procurement.values['date_planned'])
            supplier = False
            if procurement.values.get('supplierinfo_id'):
                supplier = procurement.values['supplierinfo_id']
            elif procurement.values.get('orderpoint_id') and procurement.values['orderpoint_id'].supplier_id:
                supplier = procurement.values['orderpoint_id'].supplier_id
            else:
                supplier = procurement.product_id.with_company(procurement.company_id.id)._select_seller(
                    partner_id=procurement.values.get("supplierinfo_name"),
                    quantity=procurement.product_qty,
                    date=procurement_date_planned.date(),
                    uom_id=procurement.product_uom)
                # Fall back on a supplier for which no price may be defined. Not ideal, but better than
                # blocking the user.
            supplier = supplier or procurement.product_id._prepare_sellers(False).filtered(
                lambda s: not s.company_id or s.company_id == procurement.company_id)[:1]
            if not supplier:
                msg = _(
                    'There is no matching vendor price to generate the purchase order for product %s (no vendor defined, minimum quantity not reached, dates not valid, ...). Go on the product form and complete the list of vendors.') % (
                          procurement.product_id.display_name)
                errors.append((procurement, msg))
            partner = supplier.partner_id
            # we put `supplier_info` in values for extensibility purposes
            procurement.values['supplier'] = supplier
            procurement.values['propagate_cancel'] = rule.propagate_cancel
            domain = rule._make_po_get_domain(procurement.company_id, procurement.values, partner)
            procurements_by_po_domain[domain].append((procurement, rule))
        if errors:
            raise ProcurementException(errors)
        for domain, procurements_rules in procurements_by_po_domain.items():
            # Get the procurements for the current domain.
            # Get the rules for the current domain.
            # Their only use is to create # the PO if it does not exist.
            procurements, rules = zip(*procurements_rules)
            # Get the set of procurement origin for the current domain.
            origins = set([p.origin for p in procurements])
            # Check if a PO exists for the current domain.
            po = self.env['purchase.order'].sudo().search([dom for dom in domain], limit=1)
            company_id = procurements[0].company_id
            if not po:
                positive_values = [p.values for p in procurements if float_compare(p.product_qty, 0.0,
                                                                                   precision_rounding=p.product_uom.rounding) >= 0]
                if positive_values:
                    # We need a rule to generate the PO.
                    # However the rule generated
                    # the same domain for PO and the _prepare_purchase_order method
                    # should only uses the common rules's fields.

                    vals = rules[0]._prepare_purchase_order(company_id, origins, positive_values)
                    # The company_id is the same for all procurements since
                    # _make_po_get_domain add the company in the domain.
                    # We use SUPERUSER_ID since we don't want the current user to be follower of the PO.
                    # Indeed, the current user may be a user without access to Purchase, or even be a portal user.
                    po = self.env['purchase.order'].with_company(company_id).with_user(SUPERUSER_ID).create(
                        vals)

            po_lines_by_product = {}
            grouped_po_lines = groupby(po.order_line.filtered(
                lambda l: not l.display_type and l.product_uom == l.product_id.uom_po_id),
                key=lambda l: l.product_id.id)
            for product, po_lines in grouped_po_lines:
                po_lines_by_product[product] = self.env['purchase.order.line'].concat(*po_lines)
            po_line_values = []
            for procurement in procurements:
                po_lines = po_lines_by_product.get(procurement.product_id.id,
                                                   self.env['purchase.order.line'])
                po_line = po_lines._find_candidate(*procurement)

                if float_compare(procurement.product_qty, 0,
                                 precision_rounding=procurement.product_uom.rounding) <= 0:
                    # If procurement contains negative quantity, don't create a new line that would contain negative qty
                    continue
                # If it does not exist a PO line for current procurement.
                # Generate the create values for it and add it to a list in
                # order to create it in batch.
                print(procurement)
                partner = procurement.values['supplier'].partner_id
                po_line_values.append(self.env['purchase.order.line']._prepare_purchase_order_line_from_procurement(
                    procurement.product_id, procurement.product_qty,
                    procurement.product_uom, procurement.company_id,
                    procurement.values, po, procurement.origin))
                # Check if we need to advance the order date for the new line
                order_date_planned = procurement.values['date_planned'] - relativedelta(
                    days=procurement.values['supplier'].delay)
                if fields.Date.to_date(order_date_planned) < fields.Date.to_date(po.date_order):
                    po.date_order = order_date_planned
            self.env['purchase.order.line'].sudo().create(po_line_values)
