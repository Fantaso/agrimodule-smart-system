# import json

# class AgriSensor:
#     def __init__(self, mac, identifier, uuid):
#         self.mac = mac
#         self.identifier = identifier
#         self.uuid = uuid
#         self.json_object = {
#           "identifier": ags.identifier,
#           "mac": ags.mac
#         }
#         # time created ?

# class Measurement:
#     def __init__(self, uuid, air_temp, air_rh, air_atmopressure, air_light, soil_ph, soil_ec, soil_moisture, soil_temp, battery, latitude, longitude, updated):
#         self.uuid = uuid
#         self.battery = battery
#         self.latitude = latitude
#         self.longitude = longitude
#         self.air_temp = air_temp
#         self.air_rh = air_rh
#         self.air_atmopressure = air_atmopressure
#         self.air_light = air_light
#         self.soil_ph = soil_ph
#         self.soil_ec = soil_ec
#         self.soil_moisture = soil_moisture
#         self.soil_temp = soil_temp
#         self.updated = updated
#         self.json_object = {
#           "air": {
#             "air_temp": air_temp,
#             "air_rh": air_rh,
#             "air_atmopressure": air_atmopressure,
#             "air_light": air_light,
#           },
#           "soil": {
#             "soil_ph": soil_ph,
#             "soil_ec": soil_ec,
#             "soil_moisture": soil_moisture,
#             "soil_temp": soil_temp
#           },
#           "property": {
#             "updated": updated,
#             "battery": battery,
#             "latitude": latitude,
#             "longitude": longitude
#           }
#         }

# //////////////////////////////////////////////////////////////////////////
# Initialize AgriSensor object with MAC, Identifier and UUID
# agri_sensor1 = AgriSensor("mac001", "i001", "uuid0001")
# agri_sensor2 = AgriSensor("mac002", "i002", "uuid0002")
# agri_sensor3 = AgriSensor("mac003", "i003", "uuid0003")
# agri_sensors = [agri_sensor1, agri_sensor2, agri_sensor3]

# agri_sensors_obj = {}

# for ags in agri_sensors:
#   agri_sensors_obj[ags.uuid] = ags.json_object

# //////////////////////////////////////////////////////////////////////////
# Initialize Measurement object with AirTemperature, AirRH, etc.


# //////////////////////////////////////////////////////////////////////////

# def writeToJSONFile(path, file_name, data):
#   filePathNameExt = './' + path + '/' + file_name + '.json'
#   with open(filePathNameExt, 'w') as fp:
#     json.dump(data, fp)

# path = './'
# file_name = 'agri_sensors'
# data = agri_sensors_obj

# writeToJSONFile(path, file_name, data)

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
