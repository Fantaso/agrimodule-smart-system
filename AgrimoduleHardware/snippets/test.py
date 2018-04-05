# main.py -- put your code here!
from pycom import heartbeat, rgbled
import utime

heartbeat(False)

def wlan_status_not_connected():
    for cycles in range(5):
        rgbled(0x007f00)
        utime.sleep(1)
        rgbled(0x000000)
        utime.sleep(1)
    rgbled(0x7f0000)
    utime.sleep(5)
     
while True:
    wlan_status_not_connected()
 