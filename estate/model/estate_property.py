from datetime import timedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type = fields.Many2one('estate.property.type',string='Property type')
    date_availability = fields.Date(copy = False,default=fields.Datetime.now()+timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True,default = 1000,copy = False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=False)
    property_tag = fields.Many2many('estate.property.tag',string ='property tag')
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                                  default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', index=True, tracking=True)
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'),('East','East'),('West','West')],
    )
    state = fields.Selection(
        selection=[('New','New'),('Offer Recieved','Offer Recieved'),('Offer Accepted','Offer Accepted'),('sold','sold'),('Canceled','Canceled')],default = 'New',copy=False
    )
    offers_id = fields.One2many('estate.property.offers','property_id',string='offers')
