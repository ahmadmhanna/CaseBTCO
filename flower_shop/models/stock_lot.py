from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class StockLot(models.Model):
    _inherit = 'stock.lot'

    flower_water_id = fields.One2many('flower.water', 'lot_id')

    def water_flower(self):
        self.write({'flower_water_id': [(0, 0, {'lot_id': self.id, 'watering_datetime': datetime.now()})]})


    @api.constrains('flower_water_id', 'flower_water_id.watering_datetime')
    def prevent_watering_before_time(self):
        for record in self:
            if record.product_id.flower_id:
                if len(record.flower_water_id) > 1:
                    watering_frequency = record.product_id.flower_id.watering_frequency
                    new_time = datetime.now()
                    last_watering = record.flower_water_id.sorted(key=lambda r: r.watering_datetime)[-1].watering_datetime
                    if last_watering + timedelta(days=watering_frequency) > new_time:
                        raise ValidationError('You can not water the flower now!')
                #raise ValidationError('error 2'+str(last_watering)+'|'+str(timedelta(days=watering_frequency))+'|'+str(last_watering + timedelta(days=watering_frequency))+'|'+str(new_time))


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env['product.product'].browse(vals["product_id"])
            if product.sequence_id:
                vals['name'] = product.product_tmpl_id.sequence_id.next_by_id()
        return super().create(vals_list)
