from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
import configparser
import os
from logit import logger
import sys

configFile = 'config.conf'
if os.path.exists(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
else:
    print('Error: config.conf is missing')
    sys.exit(1)

LKS_sensors = config['sensors']['lks'].split(',')
KGC_sensors = config['sensors']['kgc'].split(',')

username = config['sql']['username']
password = config['sql']['password']
database = config['sql']['database']

def connect_db():
    sqlEngine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user=username,
                                pw=password,
                                db=database))
    return sqlEngine

db = connect_db()
Session = sessionmaker(bind=db)
session = Session()



Base = declarative_base()

class maxCount(Base):
    __tablename__ = "MaxCount"
    entryID     = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date        = Column(Date, default=date.today(), nullable=False)
    hour        = Column(Integer, default=datetime.now().hour, nullable=False)
    location    = Column(String(255), nullable=False)
    maxInside   = Column(Integer, nullable=False)
    minInside   = Column(Integer, nullable=False)

class inoutCount(Base):
    __tablename__ = "InOutCount"
    entryID     = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date        = Column(Date, default=date.today(), nullable=False)
    hour        = Column(Integer, default=datetime.now().hour, nullable=False)
    location    = Column(String(255), nullable=False)
    inCount     = Column(Integer, default=0)
    outCount    = Column(Integer, default=0) 

class countHolder(Base):
    __tablename__ = "CountHolder"
    ip          = Column(String(50), primary_key=True, nullable=False)
    inCount     = Column(Integer, default=0)
    outCount    = Column(Integer, default=0) 

class liveCount(Base):
    __tablename__ = "LiveCount"
    entryID     = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date        = Column(Date, default=date.today(),nullable=False)
    location    = Column(String(50), nullable=False, primary_key=True)
    allIn       = Column(Integer, default=0)
    allOut      = Column(Integer, default=0) 
    inside      = Column(Integer, default=0) 

maxCount.__table__.create(bind=db, checkfirst=True)
inoutCount.__table__.create(bind=db, checkfirst=True)
countHolder.__table__.create(bind=db, checkfirst=True)
liveCount.__table__.create(bind=db, checkfirst=True)

def getHigherValue(a,b):
    if a > b:
        return a
    if b > a :
        return b
    if a == b:
        return a

def getLowerValue(a,b):
    if a < b:
        return a
    if b < a :
        return b
    if a == b:
        return a

f=lambda a: (abs(a)+a)/2
# z = int(f(x-y))

def updateMax(location_info, maxInside_Info):
    currentData = session.query(maxCount).filter(maxCount.location==location_info, 
                                                    maxCount.date==date.today(),
                                                    maxCount.hour == datetime.now().hour).first()
    
    if currentData is None:
        gateCount = maxCount(location=location_info,
                            hour=datetime.now().hour,
                            date=date.today(),
                            minInside=maxInside_Info,
                            maxInside=maxInside_Info)

        session.add(gateCount)
        session.commit()

    else:
        currentData.maxInside=getHigherValue(maxInside_Info,currentData.maxInside)
        currentData.minInside=getLowerValue(maxInside_Info,currentData.minInside)
        session.commit()

    # session.close()
    
    return


def updateCount(location_info, inCount_info,outCount_info):
    currentCount = session.query(inoutCount).filter(inoutCount.location==location_info, 
                                                    inoutCount.date==date.today(),
                                                    inoutCount.hour == datetime.now().hour).first()

    if currentCount is None:
        gateCount = inoutCount(location=location_info,
                            hour=datetime.now().hour,
                            date=date.today(),
                            inCount=inCount_info,
                            outCount=outCount_info)

        session.add(gateCount)
        session.commit()       
    else:
        currentCount.inCount = currentCount.inCount + int(inCount_info)
        currentCount.outCount = currentCount.outCount + int(outCount_info)
        session.commit()
    
    # session.close()

    return


def streamCount(ip_info,entry_total,exit_total):
    entryDiff=0
    exitDiff=0   
    stream_Count = session.query(countHolder).filter(countHolder.ip==ip_info).first()
    
    if stream_Count is None:
        gateCount = countHolder(ip=str(ip_info),
                    inCount=entry_total,
                    outCount=exit_total)
                    # inside=int(f(entry_total-exit_total)))

        session.add(gateCount)
        session.commit()  

    else:

        if entry_total > stream_Count.inCount:
            entryDiff = int(f(entry_total-stream_Count.inCount))
            stream_Count.inCount = entry_total
        elif entry_total < stream_Count.inCount:
            entryDiff = 0
            stream_Count.inCount = entry_total
        
        if exit_total > stream_Count.outCount:
            exitDiff = int(f(exit_total-stream_Count.outCount))
            stream_Count.outCount = exit_total
        elif exit_total < stream_Count.outCount:
            exitDiff = 0
            stream_Count.outCount = exit_total

        session.commit()
    
    if ip_info in LKS_sensors:
        gate = 'LKS'
    elif ip_info in KGC_sensors:
        gate = 'KGC'
    else:
        gate = ip_info
    
    # session.close()

    return str(gate), entryDiff, exitDiff


def liveCounter(location_info,allin_info,allout_info):
    live_Count = session.query(liveCount).filter(liveCount.location==location_info,liveCount.date==date.today()).first()

    if live_Count is None:
        gateCount = liveCount(location=location_info,
                    date=date.today(),
                    allIn=allin_info,
                    allOut=allout_info,
                    inside=int(f(allin_info-allout_info)))

        session.add(gateCount)
        session.commit()  
    else:
        live_Count.allIn = live_Count.allIn + int(allin_info)
        live_Count.allOut = live_Count.allOut + int(allout_info)
        live_Count.inside = int(f(live_Count.allIn-live_Count.allOut))

        session.commit()

    # session.close()

    return live_Count.location, live_Count.allIn, live_Count.allOut, live_Count.inside


def sumToday():
    LKS = session.query(liveCount).filter(liveCount.location=='LKS',liveCount.date==date.today()).first()
    KGC = session.query(liveCount).filter(liveCount.location=='KGC',liveCount.date==date.today()).first()
  
    if LKS:
        lks_in = LKS.allIn
        lks_out = LKS.allOut
        lks_inside = LKS.inside   
  
    if LKS:
        kgc_in = KGC.allIn
        kgc_out = KGC.allOut
        kgc_inside = KGC.inside
    
    # session.close()

    return lks_in,lks_out,lks_inside,kgc_in,kgc_out,kgc_inside


##############################################################################

def getAllMaxCount():
    try:
        allMaxCount = session.query(maxCount).all()
    except:                  
        session.rollback()
        allMaxCount = session.query(maxCount).all()
    
    
    session.close()

    return allMaxCount

def getAllInOutCount():
    AllInOutCount = session.query(inoutCount).all()
    session.close()
    return AllInOutCount
