from odoo import fields, models


class InventoryValuation(models.Model):
    _inherit = "stock.picking"
    valuation_id = fields.Many2one('stock.valuation.layer')

    def button_validate(self):
        result = super().button_validate()
        date = self.scheduled_date
        for line in self.move_ids:
            prod_id = line.product_id
            company_id = self.company_id
            moved_quantity = line.quantity_done
            user_ids = self.env['ir.config_parameter'].sudo().get_param('inventory_valuation.user_ids')
            valuation = self.env['ir.config_parameter'].sudo().get_param('inventory_valuation.valuation')
            if valuation:
                user_id = user_ids[1:-1]
                if user_id:
                    user_check = user_id.split(", ")
                    users = []
                    for partner in user_check:
                        users.append(int(partner))
                    user = self.env.user.id
                    if user in users:
                        valuation_layer = self.env['stock.valuation.layer'].create({
                            'create_date': date,
                            'quantity': moved_quantity,
                            'product_id': prod_id.id,
                            'company_id': company_id.id,
                            'unit_cost': prod_id.standard_price,
                            'value': moved_quantity * prod_id.standard_price,
                            'stock_move_id': line.id,
                            'stock_valuation_layer_id': line.stock_valuation_layer_ids.id,
                        })
                        self.valuation_id = valuation_layer.id
                        am_vals = []
                        journal_id, acc_src, acc_dest, acc_valuation = line._get_accounting_data_for_valuation()
                        print(journal_id, acc_src, acc_valuation)
                        if self.picking_type_id.sequence_code == 'INT':
                            am_vals.append(
                                line.with_company(self.company_id)._prepare_account_move_vals(acc_valuation, acc_dest,
                                                                                           journal_id, moved_quantity,f'{self.name}-{prod_id.name}',
                                                                                       self.valuation_id.id , prod_id.standard_price))
                            if am_vals:
                                account_moves = self.env['account.move'].sudo().create(am_vals)
                                account_moves._post()
        return result


