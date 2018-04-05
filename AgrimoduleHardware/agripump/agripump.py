# Agrimodule Client

# WLAN CONFIGURATION
from network import WLAN
    # Assign Static IP
import machine

# create the WLAN
wlan = WLAN(mode=WLAN.STA)


# assign static IP to WLAN
if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.1.200', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('Fantaso', auth=(WLAN.WPA2, 'PanchoVilla794'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting
# get all WLANS available and assigns static ip
wlan.ipconfig(config=('192.168.1.200', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
nets = wlan.scan()
# connects to the correct WLAN
for net in nets:
    if net.ssid == 'Fantaso':
        # WLAN FOUND
        print('WLAN {} found'.format(net.ssid))
        wlan.connect(net.ssid, auth=(net.sec, 'PanchoVilla794'), timeout = 5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        # CONNECTED TO WLAN
        print('Connected to WLAN: {}'.format(net.ssid))
        break


# Agrimodule server address and port
host = '192.168.1.79'
port = 5560

# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    command = input('Enter command: ')
    if command == 'EXIT':
        # send EXIT request to Agrimodule server
        s.send(str.encode(command))
        break
    elif command == 'KILL':
        # send KILL Command to Agrimodule Server
        s.send(str.encode(command))
        break
    s.send(str.encode(command))
    reply = s.recv(1024)
    print (reply.decode('utf-8'))
# Close the socket
s.close()
