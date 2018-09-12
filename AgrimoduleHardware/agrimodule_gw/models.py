
class AgriSensor:
    def __init__(self, mac, identifier, uuid):
        self.mac = mac
        self.identifier = identifier
        self.uuid = uuid
        self.json_object = {
          "identifier": ags.identifier,
          "mac": ags.mac
        }
        # time created ?

class Measurement:
    def __init__(self, uuid, air_temp, air_rh, air_atmopressure, air_light, soil_ph, soil_ec, soil_moisture, soil_temp, battery, latitude, longitude, updated):
        self.uuid = uuid
        self.battery = battery
        self.latitude = latitude
        self.longitude = longitude
        self.air_temp = air_temp
        self.air_rh = air_rh
        self.air_atmopressure = air_atmopressure
        self.air_light = air_light
        self.soil_ph = soil_ph
        self.soil_ec = soil_ec
        self.soil_moisture = soil_moisture
        self.soil_temp = soil_temp
        self.updated = updated
        self.json_object = {
          'air': {
            'air_temp': air_temp,
            'air_rh': air_rh,
            'air_atmopressure': air_atmopressure,
            'air_light': air_light,
          },
          'soil': {
            'soil_ph': soil_ph,
            'soil_ec': soil_ec,
            'soil_moisture': soil_moisture,
            'soil_temp': soil_temp
          },
          'property': {
            'updated': updated,
            'battery': battery,
            'latitude': latitude,
            'longitude': longitude
          }
        }
