from network import LoRa
import socket
import time

from pycom import heartbeat, rgbled
heartbeat(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

while True:
    if s.recv(64) == b'Ping':
        print('Agripump Received PING')
        rgbled(0x7f0000)
        time.sleep(1)
        s.send('Pong')
        rgbled(007f00)
        print('Agripump Sent PONG')
        time.sleep(1)
        rgbled(0x000000)
    time.sleep(5)
