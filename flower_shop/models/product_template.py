from odoo import fields, models, api
from datetime import datetime, timedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_flower = fields.Boolean()
    flower_id = fields.Many2one('flower.flower')
    need_watering = fields.Boolean(compute='_compute_need_watering')
    sequence_id = fields.Many2one('ir.sequence', 'Serial Sequence')
    gardeners_ids = fields.Many2many('res.users')

    @api.onchange('is_flower')
    def onchange_is_flower_set_flower_id(self):
        self.flower_id = False

    def _compute_need_watering(self):
        for record in self:
            record.need_watering = False
            watering_frequency = record.flower_id.watering_frequency
            if record.flower_id:
                for lot in self.env['stock.lot'].search([('product_id', 'in', record.product_variant_ids.ids)]):
                    if not lot.flower_water_id or \
                            lot.flower_water_id[-1].watering_datetime + timedelta(
                        days=watering_frequency) <= datetime.now():
                        record.need_watering = True
