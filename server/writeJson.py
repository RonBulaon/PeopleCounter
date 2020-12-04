import json
from datetime import datetime
from logit import logger

def writeToJson(lksInCount,lksOutCount,insideLKS,kgcInCount,kgcOutCount,insideKGC):
    nowdatetime = datetime.now()
    countSummary = {
        "datetime":str(nowdatetime),
        "lks":{
            "enter":str(lksInCount),
            "exit":str(lksOutCount),
            "inside":str(insideLKS)
            },
        "kgc":{
            "enter":str(kgcInCount),
            "exit":str(kgcOutCount),
            "inside":str(insideKGC)
            },
        }
    logger('INFO','receiveCount','About to update count.json!')
    try:
        logger('INFO','receiveCount','Updating count.json')
        with open('public/count.json', 'w') as outfile:
            json.dump(countSummary, outfile)
    except:
        logger('ERROR','receiveCount','Somethng went wrong while updating count.json!')