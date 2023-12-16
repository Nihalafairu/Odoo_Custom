from odoo import fields, models


class ToleranceStock(models.Model):
    """to add tolerance in the stock move lines"""
    _inherit = "stock.move"

    tolerance = fields.Integer(related='sale_line_id.tolerance')


class TolerancePicking(models.Model):
    _inherit = "stock.picking"
    accept_check = fields.Boolean(default=False)

    def button_validate(self):
        """wizard pop up when tolerance condition are mismatched"""
        for records in self.move_ids_without_package:
            if ((records.quantity_done > (records.tolerance + records.product_uom_qty)) or
                    (records.quantity_done < (records.product_uom_qty - records.tolerance))):
                if not self.accept_check:
                    print(self.accept_check, "first validate")
                    return {
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'tolerance.wizard',
                        'view_id': self.env.ref('tolerance.tolerance_wizard_form').id,
                        'target': 'new',
                        'context': {
                            'default_stock_id': self.id,
                        }
                    }
                else:
                    return super().button_validate()
            else:
                self.accept_check = True
                return super().button_validate()
