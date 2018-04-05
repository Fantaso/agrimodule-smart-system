from pycom import rgbled, heartbeat
import utime
heartbeat(False)
def wlan_status_connected():
    for cycles in range(5): # stop after 10 cycles
        rgbled(0x007f00) # green
        utime.sleep(1)
        rgbled(0x000000) # yellow
        utime.sleep(1.5)
    rgbled(0x7f0000)
    utime.sleep(3)

while True:
    wlan_status_connected()
