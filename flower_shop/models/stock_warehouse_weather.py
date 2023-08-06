from odoo import fields, models, api
from datetime import datetime

class warehouseweather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'weather'

    warehouse_id = fields.Many2one('stock.warehouse')
    temperature = fields.Float()
    pressure = fields.Float()
    humidity = fields.Float()
    wind_speed = fields.Float()
    rain_volume = fields.Float()
    capture_time = fields.Datetime()

class warehouse(models.Model):
    _inherit = 'stock.warehouse'

    weather_ids = fields.One2many('stock.warehouse.weather', 'warehouse_id')

    def get_weather_data(self):
        for record in self.get_location_warehouses():
            api_key, lat, lng = record.get_api_params()
            url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lng, api_key)
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                entries = response.json()
                self.env["stock.warehouse.weather"].create({
                    "warehouse_id": record.id,
                    "pressure": entries["main"]["pressure"],
                    "temperature": entries["main"]["temp"],
                    "humidity": entries["main"]["humidity"] / 100,
                    "wind_speed": entries["wind"]["speed"],
                    "rain_volume": entries["rain"]["1h"] if "rain" in entries else 0,
                    "capture_time": fields.Datetime.now(),
                })
            except:
                continue

    def today_forecast_for_water_flowers(self):
        date_format = '%Y-%m-%d %H:%M:%S'
        nine_AM_datetime = datetime.now().replace(hour=9, minute=0, second=0)
        six_PM_datetime = datetime.now().replace(hour=18, minute=0, second=0)
        for record in self.get_location_warehouses():
            api_key, lat, lng = record.get_api_params()
            url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lng, api_key)
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                entries = response.json()
                entries = list(filter(lambda x:  nine_AM_datetime <= datetime.strptime(x['dt_txt'],
                                                                                            date_format) <= six_PM_datetime, entries['list']))
                entries = list(filter(lambda x: 'rain' in x and x['rain']['3h'] > 0.2, entries))
                if entries:
                    flowers_serial = self.env['stock.quant'].search([('warehouse_id', '=', record.id)]).lot_id
                    flowers_serial.water_flower()
            except:
                continue

    def get_api_params(self):
        self.ensure_one()
        api_key = self.env["ir.config_parameter"].sudo().get_param("coreline_btco.weather_key")
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

    def get_location_warehouses(self):
        return self.filtered(
            lambda x: x.partner_id and x.partner_id.partner_latitude and x.partner_id.partner_longitude)