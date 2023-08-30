from odoo import models, fields

class FlowerWater(models.Model):
    _name = 'flower.water'
    _description = 'Flower Watering'

    date = fields.Date(string="Watering Date", default=fields.Date.context_today)
    lot_id = fields.Many2one('stock.lot', string="Plant")
