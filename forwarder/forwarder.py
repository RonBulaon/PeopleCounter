# python.exe gateway.py
import socket
import sys
import xml.etree.ElementTree as ET

import datetime
import logging

logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG)

x = datetime.datetime.now()

remoteServer = '<remote_IP>'
remotePort = 8080

localServer = '<local_IP>'
localPort = 443

def sendToCloud(ip,enter,exit):
    x = datetime.datetime.now()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteServer, remotePort))
    data =str(str(ip)+','+str(enter)+','+str(exit))
    print(str(x) + ',' + data)
    logging.debug(str(x) + ',' + data)

    s.send(bytes(data,"utf-8"))
    s.close()
    return

def sendRaw(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteServer2, remotePort2))
    print(data)
    s.send(data)
    s.close()
    return

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (localServer,localPort)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            sensorCounter = '<?xml version="1.0"?>' + str(data.decode('ascii')).replace('\r\n',' ').split('<?xml version="1.0"?>')[-1]
            xmlData = ET.fromstring(sensorCounter)

            ipAddress = str(xmlData[0][1].text)

            for RTCount in xmlData.iter('RTCount'):
                totalEnters = int(RTCount.attrib['TotalEnters'])
                totalExits = int(RTCount.attrib['TotalExits'])

            for RTObject in xmlData.iter('RTObject'):
                name = str(RTObject.attrib['Name'])

            try:
                sendToCloud(ipAddress,totalEnters,totalExits)
            except Exception as e:
                print('Could not send data to cloud! %s' % e)


            if data:
                break

    finally:
        # Clean up the connection
        connection.close()
