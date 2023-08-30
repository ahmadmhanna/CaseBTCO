from odoo import models, fields,api

class FlowerShop(models.Model):
    _name = 'flower.shop'
    _description = 'Flower Shop'
    
    name = fields.Char()
    season_start = fields.Date()
    season_end = fields.Date()
    watering_frequency = fields.Integer(help="Frequency is in number of days")
    scientific_name = fields.Char(required=True, translate=True, copy=False)
    watering_amount = fields.Float(required=True, help="In milmeter")
    def name_get(self):
        return [(record.id, '%s (%s)' % (record.name, record.scientific_name)) for record in self]