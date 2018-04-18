from network import LoRa
import socket
import time

from pycom import heartbeat, rgbled
heartbeat(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

s.setblocking(False)

host = ''
port 5560

storedValue = "Hey man"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Created")
    try:
        s.bind(host, port)
    except socket.error as e:
        print(e)
    print("Socket Bind Created")
    return s

def setupConnection():
    s.listen(1) #allows only 1 connection at the time
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" +str(address[1]))
    return conn

def GET():
    reply = storedValue
    return reply

def REPEAT(dataMessage):
    reply = dataMessage[1]
    return reply

def dataTransfer():
    #big loop to send sends/receive data unitl told not to.
    while True:
        # Receive data
        data = conn.recv(1024)
        data = data.decode('utf-8')
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'GET':
            reply = GET()
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
        elif command == 'EXIT':
            print("Agrimodule Client Disconnected!")
        elif command == 'KILL':
            print("Shutting Down Server")
            s.close()
            break
        else:
            reply = 'Unknown Command'
        conn.sendall(str.encode(reply))
        print('Data has been sent!')


s = setupServer()

while True:
    try:
        conn = setupConnection()
    except:
        break
