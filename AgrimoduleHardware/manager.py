import json

class AgriSensor:
    def __init__(self, mac, identifier, uuid):
        self.mac = mac
        self.identifier = identifier
        self.uuid = uuid

class Measurement:
    def __init__(self, uuid, air_temp, air_rh, air_atmopressure, air_light, soil_ph, soil_ec, soil_moisture, soil_temp, battery, latitude, longitude):
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


# //////////////////////////////////////////////////////////////////////////
# Initialize AgriSensor object with MAC, Identifier and UUID
agri_sensor1 = AgriSensor("mac001", "i001", "uuid0001")
agri_sensor2 = AgriSensor("mac002", "i002", "uuid0002")
agri_sensor3 = AgriSensor("mac003", "i003", "uuid0003")
agri_sensors = [agri_sensor1, agri_sensor2, agri_sensor3]

agri_sensors_obj = {}

for ags in agri_sensors:
  # Info of an agri_sensor
  agri_sensor_obj = {
    "identifier": ags.identifier,
    "mac": ags.mac
  }
  agri_sensors_obj[ags.uuid] = agri_sensor_obj

# //////////////////////////////////////////////////////////////////////////
# Initialize Measurement object with AirTemperature, AirRH, etc.
measurement1 = Measurement("uuid001", 25, 10, 12, 15, 12, 3, 7, 13, 0.72, 35.6895, 139.6917)
measurement2 = Measurement("uuid002", 22, 12, 11, 14, 11, 1, 7, 9, 0.70, 35.6895, 139.6917)
measurement3 = Measurement("uuid003", 12, 22, 13, 11, 10, 1, 4, 10, 0.71, 35.6895, 139.6917)
measurements = [measurement1, measurement2, measurement3]

measurements_obj = {
  "reported": {
  }
}

# A measurement
for m in measurements:
  measurement_obj = {
    "air": {
      "air_temp": m.air_temp,
      "air_rh": m.air_rh,
      "air_atmopressure": m.air_atmopressure,
      "air_light": m.air_light,
    },
    "soil": {
      "soil_ph": m.soil_ph,
      "soil_ec": m.soil_ec,
      "soil_moisture": m.soil_moisture,
      "soil_temp": m.soil_temp
    },
    "property": {
      "battery": m.battery,
      "latitude": m.latitude,
      "longitude": m.longitude
    }
  }
  measurements_obj['reported'][m.uuid] = measurement_obj



# //////////////////////////////////////////////////////////////////////////

def writeToJSONFile(path, file_name, data):
  filePathNameExt = './' + path + '/' + file_name + '.json'
  with open(filePathNameExt, 'w') as fp:
    json.dump(data, fp)

path = './'
file_name = 'agri_sensors'
data = agri_sensors_obj

writeToJSONFile(path, file_name, data)

# shadow_obj =
# {
#   "reported": {
#     "AgriSensors": {
#       "uuid": "as001": {
#         "air": {
#           "air_temp": 25,
#           "air_rh": 10,
#           "air_atmopressure": 12,
#           "air_light": 15
#         },
#         "soil": {
#           "soil_ph": 12,
#           "soil_ec": 3,
#           "soil_moisture": 7,
#           "soil_temp": 13,
#         },
#         "property": {
#           "battery": 0.75
#           "coordinates": {
#             "lat": 35.6895,
#             "lng": 139.6917
#           }
#         }
#       },
#       "uuid": "as001": {
#         "air": {
#           "air_temp": 20,
#           "air_rh": 11,
#           "air_atmopressure": 13,
#           "air_light": 12
#         },
#         "soil": {
#           "soil_ph": 11,
#           "soil_ec": 2,
#           "soil_moisture": 5,
#           "soil_temp": 13,
#         },
#         "property": {
#           "battery": 0.75
#           "coordinates": {
#             "lat": 35.6895,
#             "lng": 139.6917
#           }
#         }
#       },
#       "uuid": "as001": {
#         "air": {
#           "air_temp": 19,
#           "air_rh": 19,
#           "air_atmopressure": 8,
#           "air_light": 12
#         },
#         "soil": {
#           "soil_ph": 14,
#           "soil_ec": 1,
#           "soil_moisture": 5,
#           "soil_temp": 17,
#         },
#         "property": {
#           "battery": 0.72
#           "coordinates": {
#             "lat": 35.6895,
#             "lng": 139.6917
#           }
#         }
#       },
#       "uuid": "as001": {
#         "air": {
#           "air_temp": 21,
#           "air_rh": 18,
#           "air_atmopressure": 10,
#           "air_light": 10
#         },
#         "soil": {
#           "soil_ph": 12,
#           "soil_ec": 3,
#           "soil_moisture": 7,
#           "soil_temp": 11,
#         },
#         "property": {
#           "battery": 0.65
#           "coordinates": {
#             "lat": 35.6895,
#             "lng": 139.6917
#           }
#         }
#       },
#       "uuid": "as001": {
#         "air": {
#           "air_temp": 22,
#           "air_rh": 11,
#           "air_atmopressure": 10,
#           "air_light": 11
#         },
#         "soil": {
#           "soil_ph": 10,
#           "soil_ec": 1,
#           "soil_moisture": 4,
#           "soil_temp": 10,
#         },
#         "property": {
#           "battery": 0.42
#           "coordinates": {
#             "lat": 35.6895,
#             "lng": 139.6917
#           }
#         }
#       }
#     }
#   }
# }
