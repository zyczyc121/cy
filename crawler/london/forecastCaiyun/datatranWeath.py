#coding:utf-8
#    date: 20180303
#    author: maxtri
#    function: 获取london 天气数据可以处理指定日期，处理某一天的数据，
#              也可以不指定日期，只处理当天的数据，
#              处理结果存放在$path的同目录下
#
#    使用方法:
#               python ./trancData.py  [option] [date]               
#               [option]: 指定程序的功能,详见help
#               [date]: 指定要处理数据所属的秒,如: 155229935 或者 today
#              
#
#

# 获取london 各气象站点的QAI数据
import pandas as pd
import sys as sys
import json as json
from datetime import datetime
import time as time 
import urllib2


# 获取的空气指标
_weatherList = ['skycon','temperature','pres','humidity','direction','speed']

# 获取的天气站点名称
_stationList = []
lineStations = open('./stationId')
for line in lineStations:
    tmp = []
    tmp.append(line.split(',')[0])
    tmp.append(line.split(',')[1])
    tmp.append(line.split(',')[2].strip('\n'))
    _stationList.append(tmp)

# 获取某一时刻的天气预报
def getWeatherOneDay( curTime, _stationList):
    newOneHourData= []
    aqiStationData = []
    for city,lat,lng in _stationList:
        try:
            s = urllib2.urlopen("https://api.caiyunapp.com/v2/96Ly7wgKGq6FhllM/%s,%s/weather?begin=%s&tzshift=0&hourlysteps=73" %(lng,lat,curTime)).read()
            #lines = open(path)
        except:
            continue

        tmp = []
            # 检查文件是否为完整的json
        try:
            d = json.loads(s)
        except:
            continue
                
        if d['status'] == 'failed':
                continue

        for itr in range(1,73):
            tmp = []
            tmp.append(city)
            tmp.append(datetime.utcnow().strftime("%Y"))
            tmp.append(datetime.utcnow().strftime("%m"))
            tmp.append(datetime.utcnow().strftime("%d"))
            tmp.append(datetime.utcnow().strftime("%H"))
            tmp.append(d['result']['hourly']['skycon'][itr]['datetime'].split(' ')[0].split('-')[0])
            tmp.append(d['result']['hourly']['skycon'][itr]['datetime'].split(' ')[0].split('-')[1])
            tmp.append(d['result']['hourly']['skycon'][itr]['datetime'].split(' ')[0].split('-')[2])
            tmp.append(d['result']['hourly']['skycon'][itr]['datetime'].split(' ')[1].split(':')[0])
            
            # 添加weather
            tmp.append(d['result']['hourly']['skycon'][itr]['value'])
            tmp.append(d['result']['hourly']['temperature'][itr]['value'])
            tmp.append(d['result']['hourly']['pres'][itr]['value']/100)
            tmp.append(d['result']['hourly']['humidity'][itr]['value']*100)
            tmp.append(d['result']['hourly']['wind'][itr]['direction'])
            tmp.append(d['result']['hourly']['wind'][itr]['speed'])
            aqiStationData.append(tmp)
        #newOneHourData.append(tmp)
    newOneHourDataPD = pd.DataFrame(aqiStationData, \
                                   columns=['city', 'Year', 'Mon','Day','Hour',\
                         'forecast_Year', 'forecast_Mon','forecast_Day','forecast_Hour',\
                                            'weather','temp_c','pressure_mb',\
                          'relative_humidity','wind_degrees','wind_kph' ])
    beijingHour = datetime.now().strftime('%Y%m%d%H')
    newOneHourDataPD.to_csv('/home/yichengkeg/kdd/clean/londonAir_realtime' + '/' +  \
                              beijingHour  + '_me_forecast.csv',index=False)

def getWeatherToday(_cityList):
    today = datetime.now().strftime('%s')
    data = getWeatherOneDay( today, _cityList)  

def main():
   helpInfo =  " Use:   \n"
   helpInfo += "     -s   specify one day data processing \n" 
   helpInfo += "          eg. python ./datatranWeath.py  -s  155278997 \n"
   helpInfo += "     -t   deal today data set \n"
   helpInfo += "          eg. python ./datatranWeath.py  -t today  \n"
   helpInfo += "     -h   print help info \n"
   
   if len(sys.argv) != 3:
       print(helpInfo) 
       return -1
   date = sys.argv[2]

   if sys.argv[1] == '-t' and len(sys.argv) == 3:
       _data = getWeatherToday( _stationList) 

   elif sys.argv[1] == '-s' and len(sys.argv) ==3:
       _data = getWeatherOneDay(  date, _stationList)

   else:
       print(helpInfo)
   return 0

if __name__ == "__main__":
    main()

