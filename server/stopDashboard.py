import subprocess
import sys
import os
import time
os.chdir('/home/ltiadmin/LiveOccupancyCounter/')

from logit import logger
logger('INFO','checker','Stopping Dashboard!')

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
else:
    subprocess.check_output("kill -9 %s" % port8002, shell=True)
    time.sleep(5)
    startDasboard()
    

if port8002 == 0:
    startDasboard()

sys.exit(1) 
