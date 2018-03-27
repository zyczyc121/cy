# -*- coding: latin-1 -*-
#    func: 获取londonAir 的每小时数据和每日数据#
#
#
#
#
#
#
import pandas as pd
import numpy as np
import json as  json
import sys as sys
import math
from  datetime import datetime

siteCodes = ['CD1','BL0','GR4', 'MY7', 'HV1', 'GN3', 'GR9', 'LW2', 'GN0', 'KF1', 'CD9', 'CT3', 'CT2','BX9','BX1' ]
siteCodesS = ['BX9', 'BX1']

def getSpecifyDay(filespath,date,siteCodes):
  dataHour = []
  for site in siteCodes:
    path = filespath + date + '/' + str(site) + '_' + date + '.log' 
    lines = open(path)
    for line in lines:
        try:
            lineJsons = json.loads(line)
        except:
             continue
        Ipm25 = []
        Ipm10 = []
        Ino2 = []
        for lineJson in lineJsons['AirQualityData']['Data']:
            Ipm25tmp = []
            Ipm10tmp = []
            Ino2tmp = []
            if lineJson['@SpeciesCode'] == 'PM25':
                Ipm25tmp.append(lineJson['@MeasurementDateGMT'].split(' ')[0].replace('-',''))
                Ipm25tmp.append(lineJson['@MeasurementDateGMT'].split(' ')[1].split(':')[0])
                Ipm25tmp.append(lineJson['@Value'])
                #print Ipm25tmp
                Ipm25.append(Ipm25tmp)
            elif lineJson['@SpeciesCode'] == 'PM10':
                Ipm10tmp.append(lineJson['@MeasurementDateGMT'].split(' ')[0].replace('-',''))
                Ipm10tmp.append(lineJson['@MeasurementDateGMT'].split(' ')[1].split(':')[0])
                Ipm10tmp.append(lineJson['@Value'])
                Ipm10.append(Ipm10tmp)
            elif lineJson['@SpeciesCode'] == 'NO2':
                Ino2tmp.append(lineJson['@MeasurementDateGMT'].split(' ')[0].replace('-',''))
                Ino2tmp.append(lineJson['@MeasurementDateGMT'].split(' ')[1].split(':')[0])
                Ino2tmp.append(lineJson['@Value'])
                Ino2.append(Ino2tmp)
            else:
                continue
        Ipm25Pd = pd.DataFrame(Ipm25,columns=['date','hour','pm25'])
        Ipm10Pd = pd.DataFrame(Ipm10,columns=['date','hour','pm10'])
        Ino2Pd = pd.DataFrame(Ino2,columns=['date','hour','no2'])
        if len(Ipm25Pd) != 0:
            dataP = Ipm25Pd
            dataP = dataP.merge(Ipm10Pd, how='left',on=['date','hour'])
            dataP = dataP.merge(Ino2Pd, how='left', on=['date','hour'])
            dataP['stationId'] = site
            dataP = dataP[['stationId','date','hour','pm25','pm10','no2']]
        else: 
            dataP = Ipm10Pd
            #dataP = dataP.merge(Ipm10Pd, how='left',on=['date','hour'])
            dataP = dataP.merge(Ino2Pd, how='left', on=['date','hour'])
            #today = datetime.now().strftime('%Y%m%d')
            dataP['stationId'] = site
            dataP['pm25']  = ''
            dataP = dataP[['stationId','date','hour','pm25','pm10','no2']]
        # dataP.to_csv('./%s_clean.csv' %(today), index=False)
    if (dataP.iloc[-1].tolist()[3] == '' or math.isnan(dataP.iloc[-1].tolist()[3] == True )) \
     and (dataP.iloc[-1].tolist()[4] == '' or math.isnan(dataP.iloc[-1].tolist()[4]) == True) \
     and (dataP.iloc[-1].tolist()[5] == '' or math.isnan(dataP.iloc[-1].tolist()[5]) == True):
         dataHour.append(dataP.iloc[-2,:].tolist())
    else:
        dataHour.append(dataP.iloc[-1,:].tolist())
    if site == 'CD1':
        dataToday = dataP
    else:
        dataToday = pd.concat([dataToday, dataP])
  dataToday.to_csv('/home/yichengkeg/kdd/clean/londonAir/%s_clean.csv' %(date), index=False)
  hourDate = datetime.now().strftime('%Y%m%d%H') 
  dataHourPd = pd.DataFrame(dataHour,columns=['stationId','date','hour','pm25','pm10','no2'])
  dataHourPd.to_csv('/home/yichengkeg/kdd/clean/londonAir_realtime/%s_clean.csv' %(hourDate), index=False)


def  getAqisToday(filespath, siteCodes):
    today = datetime.now().strftime('%Y%m%d')
    data = getSpecifyDay(filespath, today, siteCodes)  

def main():
   helpInfo =  " Use:   \n"
   helpInfo += "     -s   specify one day data processing \n" 
   helpInfo += "          eg. python ./getCleanData.py  -s 20180123 /home/szw16/kdd/london/data/ \n"
   helpInfo += "     -t   deal today data set \n"
   helpInfo += "          eg. python ./getCleanData.py  -t today   /home/szw16/kdd/london/data/ \n"
   helpInfo += "     -h   print help info \n"
   
   if len(sys.argv) != 4:
       print(helpInfo) 
       return -1
   date = sys.argv[2]
   path = sys.argv[3]

   if sys.argv[1] == '-t' and len(sys.argv) == 4:
       _data = getAqisToday(path, siteCodes) 

   elif sys.argv[1] == '-s' and len(sys.argv) ==4:
       _data = getSpecifyDay(path,  date, siteCodes)

   else:
       print(helpInfo)
   return 0

if __name__ == "__main__":
    main()

