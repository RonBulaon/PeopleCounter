import subprocess
import sys
import os
os.chdir('/home/ltiadmin/LiveOccupancyCounter/')

from logit import logger
logger('INFO','checker','Checking services status!')
try:
    port8080 = subprocess.check_output("ss -lptn 'sport = :8080' | grep LISTEN", shell=True)
    port8080 = port8080.decode('ascii')
    port8080 = port8080.split('users:')[1].split(',')[1].split('=')[1]
except:
    port8080 = 0

try:
    port8001 = subprocess.check_output("ss -lptn 'sport = :8001' | grep LISTEN", shell=True,stderr=subprocess.STDOUT)
    port8001 = port8001.decode('ascii')
    port8001 = port8001.split('users:')[1].split(',')[1].split('=')[1]
except:
    port8001 = 0

try:
    port8002 = subprocess.check_output("ss -lptn 'sport = :8002' | grep LISTEN", shell=True,stderr=subprocess.STDOUT)
    port8002 = port8001.decode('ascii')
    port8002 = port8001.split('users:')[1].split(',')[1].split('=')[1]
except:
    port8002 = 0

def startApp():
    try:
        logger('CRITICAL','checker','Service is down. Now trying to start app.py')
        subprocess.Popen("nohup python3 /home/ltiadmin/LiveOccupancyCounter/app.py", shell=True,stderr=subprocess.STDOUT)
    except:
        logger('ERROR','checker','Failed to start app.py!')

if ((port8001 != 0) and (port8080 == 0)):
    try:
        subprocess.check_output("kill -9 %s" % port8001, shell=True)
    except:
        print('nothing to kill')
    
    startApp()

if ((port8080 != 0) and (port8001 == 0)):
    try:
        subprocess.check_output("kill -9 %s" % port8080, shell=True)
    except:
        print('nothing to kill')

    startApp()

if ((port8080 == 0) and (port8001 == 0)):
    startApp()

def startDasboard():
    try:
        logger('CRITICAL','checker','Service is down. Now trying to start dashboard.py')
        subprocess.Popen("nohup python3 /home/ltiadmin/LiveOccupancyCounter/dashboard.py", shell=True,stderr=subprocess.STDOUT)
    except:
        logger('ERROR','checker','Failed to start dashboard.py!')

try:
    port8002 = subprocess.check_output("ss -lptn 'sport = :8002' | grep LISTEN", shell=True,stderr=subprocess.STDOUT)
    port8002 = port8002.decode('ascii')
    port8002 = port8002.split('users:')[1].split(',')[1].split('=')[1]
except:
    port8002 = 0

if port8002 == 0:
    startDasboard()

sys.exit(1) 
