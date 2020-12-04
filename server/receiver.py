from writeToDB import streamCount, liveCounter, updateMax, updateCount, sumToday
from writeJson import writeToJson
from logit import logger
import socket
import re
import datetime
import configparser
import sys
import os

configFile = 'config.conf'
if os.path.exists(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
else:
    print('Error: config.conf is missing')
    sys.exit(1)

def checkSchedule():
    operatingHoursToday = config['schedule'][str(datetime.datetime.today().weekday())].split(',')
    if str(datetime.datetime.now().hour) in operatingHoursToday:
        return True
    else:
        return False

def sendCount(location,inCount,outCount):
    try:
        fromSensor = streamCount(location,inCount,outCount)
    except:
        pass
    else:
        try:
            logger('INFO','receiver','calling updateCount()')
            updateCount(fromSensor[0],fromSensor[1],fromSensor[2])
        except:
            logger('ERROR','receiver','unable to call or execute updateCount()')

        try:
            logger('INFO','receiver','calling liveCounter()')
            print(fromSensor[0],fromSensor[1],fromSensor[2])
            currentCount = liveCounter(fromSensor[0],fromSensor[1],fromSensor[2])
            
        except Exception as inst:
            logger('ERROR','receiver','unable to call or execute liveCounter() : %s' % inst)
        else:
            try:
                logger('INFO','receiver','calling updateMax')
                updateMax(currentCount[0], currentCount[3])
            except:
                logger('ERROR','receiver','unable to call or execute updateMax()')


    try:
        logger('INFO','receiver','calling sumToday()')
        lks_in,lks_out,lks_inside,kgc_in,kgc_out,kgc_inside = sumToday()  
        print(lks_in,lks_out,lks_inside,kgc_in,kgc_out,kgc_inside)
    except:
        logger('ERROR','receiver','unable to call or execute sumToday()')
    else:
        try:
            if checkSchedule():
                writeToJson(lks_in,lks_out,lks_inside,kgc_in,kgc_out,kgc_inside)  
            else:
                writeToJson(0,0,0,0,0,0)  
        except:
            logger('ERROR','receiver','unable to call or execute writeToJson()')
    return 


def receiveCount():
    packetPatern=re.compile('(?:\d{1,3}\.){3}\d{1,3},[0-9]+,[0-9]+')

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    try:
        server_address = ('0.0.0.0',8080)
        logger('INFO','receiveCount','starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)
        logger('INFO','receiveCount','Listening in at %s port %s' % server_address)
    except:
        logger('ERROR','receiveCount',('Unable to bind on %s port %s' % server_address))

    while True:
        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(1024) 
                try:
                    if packetPatern.match(data.decode("utf-8")):
                        logger('INFO','receiveCount','Data receiuved from %s' % str(client_address))
                        try:
                            ipAddress = str(data, 'utf-8').split(',')[0]
                            totalEnters = int(str(data, 'utf-8').split(',')[1])
                            totalExits = int(str(data, 'utf-8').split(',')[2])
                        except:
                            logger('WARNING','receiveCount','unable to parse received data %s' % str(client_address))
                    else:
                        logger('WARNING','receiveCount',('a String with different pattern was received. \n %s' % data.decode("utf-8")))

                    try:
                        logger('INFO','receiveCount',('Received Data from %s' % ipAddress))
                        sendCount(ipAddress,totalEnters,totalExits)
                    except:
                        logger('ERROR','receiveCount','Something went wrong! Unable to call checkCount')
                except:
                    logger('ERROR','receiveCount','Could not decode byte')

                if data:
                    break
            
        finally:
            # Clean up the connection
            connection.close()