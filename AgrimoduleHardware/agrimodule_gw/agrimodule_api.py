
# This API is in Rasp Pi
# Rasp to APP communication

import requests
from getmac import get_mac_address
from os import path
import json


# METHODS
def get_mac(wifi_interface):
    return get_mac_address(interface = wifi_interface)


# API VARIABLES
headers = {'Content-type': 'application/json'}

# API
def index(url):
    # just to check if the API works
    r = requests.get(url, headers = headers)
    return r

def check(url, identifier):
    # check for validation on agrimodule
    # checks wether the agrimodule has a valid license, bolong to other farmer, etc
    url = path.join(url, identifier)
    r = requests.get(url, headers = headers)
    return r

def register(url, payload):
    # register an agrimodule when all the validation has been checked.
    r = requests.post(url, data = payload, headers = headers)
    return r


# CONFIRATION DATA
wifi_interface = 'wlan0'

# AGRIMODULE DATA
identifier = 'agtest3'
mac = get_mac_address(wifi_interface)

# SERVER DATA
url = 'http://192.168.1.17:5000/agrimodule_api'
url_check = url + '/check'
url_register = url + '/register'


#####################################
#####################################
print('-------------------------')
print('MAC-ADDRESS:   ' + mac)
print('AG-IDENTIFIER: ' + identifier)
print('')
print('URL:           ' + url)
print('URL-CHECK:     ' + url_check)
print('URL-REGISTER:  ' + url_register)
print('')

# SAY HELLO TO API
index = index(url)
check = check(url_check, identifier)

payload = json.dumps(dict(identifier = identifier, mac = mac))
register = register(url_register, payload)
# register = register()

print('-------------------------')
print('INDEX:      ' + index.text)
print('CHECK:      ' + check.text)
print('REGISTER:   ' + register.text)
print('')


# Store UUID in some kind of a file, in order not to lose it.





