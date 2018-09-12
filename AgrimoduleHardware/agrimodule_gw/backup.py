import json

agri_sensor1 = AgriSensor("mac001", "i001", "uuid0001")
agri_sensor2 = AgriSensor("mac002", "i002", "uuid0002")
agri_sensor3 = AgriSensor("mac003", "i003", "uuid0003")
agri_sensors = [agri_sensor1, agri_sensor2, agri_sensor3]

agri_sensors_obj = {}

for ags in agri_sensors:
  agri_sensors_obj[ags.uuid] = ags.json_object

def writeToJSONFile(path, file_name, data):
  filePathNameExt = './' + path + '/' + file_name + '.json'
  with open(filePathNameExt, 'w') as fp:
    json.dump(data, fp)

path = './'
file_name = 'agri_sensors'
data = agri_sensors_obj

writeToJSONFile(path, file_name, data)
