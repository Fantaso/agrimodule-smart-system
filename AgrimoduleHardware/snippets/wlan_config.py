import machine, utime
from network import WLAN
from pycom import heartbeat, rbgled # for conrtolling the led
from mycropython import const

heartbeat(False) # deactivate default blinking led from lopy
_YELLOW = const(0x7f7f00)
# _BLUE = const(0x0000FF)
# _WHITE = const(0xffffff)
_GREEN = const(0x007f00)
_RED = const(0x7f0000)
_OFF = const(0x000000)

# STATIC IP CONFIGURATION
IP = '192.168.1.15'
MASK = '255.255.255.0'
GATEWAY = '192.168.1.1'
DNS_SERVER = '192.168.1.1'
# WIFI CONFIGURATION
SSID = 'Fantaso'
SSID_PASS = 'PanchoVilla794'

# configure the WLAN as a client (default is AP)
wlan = WLAN(mode=WLAN.STA)
# configure the WLAN with Static IP address
wlan.ifconfig(config = (IP, MASK, GATEWAY, DNS_SERVER))

# STATUS LED INDICATOR FOR WLAN CONFIGURATION
def wlan_status_not_found():
    for i in range(5):
        rbgled(_RED)
        utime.sleep(0.2)
        rbgled(_OFF)
        utime.sleep(0.2)

def wlan_status_waiting():
    for i in range(5):
        rbgled(_YELLOW)
        utime.sleep(0.2)
        rbgled(_OFF)
        utime.sleep(0.2)

def wlan_status_connected():
    for i in range(5):
        rbgled(_GREEN)
        utime.sleep(0.2)
        rbgled(_OFF)
        utime.sleep(0.2)


# WLAN CONFIGURATION
def wlan_config():
    if wlan.isconnected():
        print('Already connected to SSID: {}'.format(SSID))
        return
    else:
        nets = wlan.scan() # scan for available networks
        for net in nets:
            if net.ssid == SSID:
                print('SSID {} Found'.format(SSID))
                wlan.connect(ssid = SSID, auth = (WLAN.WPA2, SSID_PASS))
                while not wlan.isconnected():
                    print('Waiting to connect!')
                    wlan_status_waiting()
                    utime.sleep(0.5)
                    machine.idle() # save power while waiting
                print('Connected to {} with IP {}'.format(SSID,IP))
                wlan_status_connected()
                return
        print('SSID {} NOT FOUND!'.format(SSID))
        wlan_status_not_found()

if __main__ == '__name__':
    wlan_config()
