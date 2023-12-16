from odoo import fields, models

class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Estate Property Offers"

    price = fields.Float()
    status = fields.Selection(
        selection=[('Refused','Refused','Accepted','Accepted')],copy = False
    )
    partner_id = fields.Many2one('res.partner',string='partner',required = True)
    property_id = fields.Many2one('estate.property',string='property_id',required=True)

















