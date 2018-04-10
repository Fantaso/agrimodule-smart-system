from network import LoRa
import socket
import time

from pycom import heartbeat, rgbled
heartbeat(False)

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
while True:
    print('Agrimodule Sending PING')
    rgbled(0x007f00)
    time.sleep(1)
    s.send('Ping')
    rgbled(0x000000)
    time.sleep(5)

    