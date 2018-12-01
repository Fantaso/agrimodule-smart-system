import json

def writeToJSONFile(path, file_name, data):
  filePathNameExt = './' + path + '/' + file_name + '.json'
  with open(filePathNameExt, 'w') as fp:
    json.dump(data, fp)

