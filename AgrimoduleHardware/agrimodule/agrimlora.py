from network import LoRa
import socket
import time

from pycom import heartbeat, rgbled
heartbeat(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


while True:
    print('Agrimodule Sending PING')
    rgbled(0x007f00)
    time.sleep(1)
    s.send('Ping')
    rgbled(0x000000)
    if s.recv(64) == b'Pong':
        time.sleep(1)
        print('Agrimodule Received PONG')
        rgbled(0x7f0000)
        time.sleep(1)
        rgbled(0x000000)
    time.sleep(5)

    