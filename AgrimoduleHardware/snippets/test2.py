# main.py -- put your code here!
from pycom import heartbeat, rgbled
import utime

heartbeat(False)

def wlan_status_waiting():
    for times in range(5):
        rgbled(0x7f7f00)
        utime.sleep(0.6)
        rgbled(0x000000)
        utime.sleep(0.2)
        print('I am waiting')

def wlan_status_not_connected():
    for times in range(5):
        rgbled(0x7f0000)
        utime.sleep(0.6)
        rgbled(0x000000)
        utime.sleep(0.2)
        print('I am NOT connected')
        
def wlan_status_connected():
    for times in range(5):
        rgbled(0x007f00)
        utime.sleep(0.6)
        rgbled(0x000000)
        utime.sleep(0.2)
        print('I am connected')
        

while True:
    wlan_status_not_connected()
    wlan_status_waiting()
    wlan_status_connected()
    rgbled(0x000000)
    print('I am SLEEPING')
    utime.sleep(3)
