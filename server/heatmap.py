import pandas as pd
from datetime import date, timedelta, datetime
from writeToDB import getAllMaxCount, getAllInOutCount

dateToStart = [2020,9,18]
hours = list(range(6,24))

def readableTime():
    hourLabels = []
    for index, hour in enumerate(hours):
        if int(hour) < 12:
            x = str(hour) +' AM'
        if int(hour) > 12:
            x = str(hour-12) +' PM'
        if int(hour) == 12:
            x = str(hour) +' PM'
        
        hourLabels.append(x)
    return hourLabels

def dateFromStart():
    startDate = date(dateToStart[0],dateToStart[1],dateToStart[2])
    dates = []
    while True:
        dates.append(startDate)
        startDate = startDate + timedelta(days=1) 
        if startDate == date.today():
            dates.append(startDate)
            break
    return dates

def dateDays():
    dates = dateFromStart()
    getDay = []
    for date in dates:
        getDay.append(str(date.strftime('%d %b %a')))
    return getDay


def heatmapData(lib):
    from datetime import date
    maxInsideData = pd.DataFrame()

    rows_list = []
    for each in getAllMaxCount():
        rows_list.append([each.location, each.date, each.hour, each.maxInside, each.minInside])

    maxInsideData = pd.DataFrame(rows_list)
    maxInsideData.columns = ['Location','date','hour','max','min']

    if lib == "LKS":
        data = maxInsideData[(maxInsideData['Location'] == 'LKS')]
    if lib == "KGC":
        data = maxInsideData[(maxInsideData['Location'] == 'KGC')]  

    dates = dateFromStart()

    hourlyMax = []
    for hour in hours:
        dayHours = []
        for date in dates:
            try:
                max = int(data[(data['date'] == date) & (data['hour'] == hour)]['max'])
            except:
                dayHours.append(0)
            else:
                dayHours.append(max) 
        hourlyMax.append(dayHours)        

   
    return hourlyMax,dateDays(), readableTime()

def tableData(lib):
    rows_list = []
    for each in getAllMaxCount():
        rows_list.append([each.location, each.date, each.hour, each.maxInside, each.minInside])

    maxInsideData = pd.DataFrame(rows_list)
    maxInsideData.columns = ['Location','Date','Hour','Max','Min']

    rows_list = []
    for each in getAllInOutCount():
        rows_list.append([each.date, each.hour, each.location, each.inCount, each.outCount])


    inoutData = pd.DataFrame(rows_list)
    inoutData.columns = ['Date','Hour','Location','In','Out']

    result = pd.merge(maxInsideData, inoutData)
    result = result[(result['Location'] == lib) & (result['Date'] >= date(dateToStart[0],dateToStart[1],dateToStart[2])) & (result['Hour'] > 5) ]

    return result 

