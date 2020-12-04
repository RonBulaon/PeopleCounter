import datetime 
import os
import configparser
import pymsteams
import sys

configFile = 'config.conf'
if os.path.exists(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
else:
    print('Error: config.conf is missing %s' % configFile)
    sys.exit(1)


def logger(level,function,msg):
    if datetime.datetime.now().hour == 17:
        logRetention()

    now = datetime.datetime.now()
    filename = str(config['log']['logprefix'])+'.'+str(now.strftime("%d"))+'-'+str(now.strftime("%b"))+'-'+str(now.year)+'.log'

    path = 'logs/'+filename

    if os.path.exists(path):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    logentry=('[' +  str(now.strftime("%d.%b.%Y %H:%M:%S")) + '] : [' + level + '] [' + function + '] '+ msg + '\n')

    def writeLog(logentry):
        try:
            myFile = open(path, append_write) # or 'a' to add text instead of truncate    
            myFile.write(logentry)
            myFile.close()
        except:
            print('Error : Unable to write to log file.') 
            return

    if int(config['log']['debug']) == 1:
        writeLog(logentry)
        print(logentry)
    else:
        logLvels = ['WARNING','ERROR','CRITICAL']
        if function in logLvels:
            sendToMSTeams(logentry)
            writeLog(logentry)
            print(logentry)
           
    return


def logRetention():
    # print(os.listdir('logs'))
    now = datetime.datetime.now()
    filenames=os.listdir('logs')
    for file in filenames:
        date_str = file.split('.')[1]
        try:
            createdDate = datetime.datetime.strptime(date_str, '%d-%b-%Y')      
            age = now - createdDate
            if age.days >= int(config['log']['rotate']):
                # print(file)
                try:
                    os.remove('logs/'+file)
                    logger('INFO','logRetention',('deleted %s' % file) )
                except:
                    logger('ERROR','logRetention',('unable to delete logfile %s' % file) )
        except:
            logger('ERROR','logRetention',('%s is not a log file!' % file))
    
    return
            

def sendToMSTeams(msg):
    try:
        if config['msteams']['webhook']:
            myTeamsMessage = pymsteams.connectorcard(config['msteams']['webhook'])
            myTeamsMessage.text(msg)
            myTeamsMessage.send()
        else:
            logger('ERROR','sendToMSTeams','MS Teams webhook is missing' )
    except:
        logger('ERROR','logit','Unable to send MS Teams notification!' )
    return


# logger('TEST','logit','This is a test!')