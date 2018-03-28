#coding:utf-8
#    date: 20180303
#    author: maxtri
#    function: 获取london 天气数据可以处理指定日期，处理某一天的数据，
#              也可以不指定日期，只处理当天的数据，
#              处理结果存放在$path的同目录下
#
#    使用方法:
#               python ./trancData.py  [option] [date]  [path]              
#               [option]: 指定程序的功能,详见help
#               [date]: 指定要处理数据所属的日志,如: 20180214 或者 today
#               [path]: 指定源数据所在的路径,如: /data/test/kdd/
#
#

# 获取london 各气象站点的QAI数据
import pandas as pd
import sys as sys
import json as json
from datetime import datetime
import time as time 

# 获取的空气指标
_weatherList = ['skycon','temperature','pres','humidity','direction','speed']

# 获取的天气站点名称
_stationList = []
lineStations = open('./stationId')
for line in lineStations:
    _stationList.append(line.split(',')[0])

# 或缺指定date的天气
def getWeatherOneDay(filespath, date, _stationList):
    newOneHourData= []
    aqiStationData = []
    for city in _stationList:
        try:
            path = filespath + date + '/' + str(city) + '_' + date + '.log' 
            #lines = open(path)
        except:
            continue
        lines = open(path)

        for line in lines:
            tmp = []
            # 检查文件是否为完整的json
            try:
                d = json.loads(line)
            except:
                continue
                
            # 添加时间
            if d['status'] == 'failed':
                continue
            tmp.append(city)
            #tmp.append(d['current_observation']['observation_time_rfc822'].split(',')[1])
            tmp.append(datetime.utcfromtimestamp(d['server_time']).strftime("%Y"))
            tmp.append(datetime.utcfromtimestamp(d['server_time']).strftime("%m"))
            tmp.append(datetime.utcfromtimestamp(d['server_time']).strftime("%d"))
            tmp.append(datetime.utcfromtimestamp(d['server_time']).strftime("%H"))
            # 添加weather
            tmp.append(d['result']['skycon'])
            tmp.append(d['result']['temperature'])
            tmp.append(d['result']['pres']/100)
            tmp.append(d['result']['humidity']*100)
            tmp.append(d['result']['wind']['direction'])
            tmp.append(d['result']['wind']['speed'])
            aqiStationData.append(tmp)
        newOneHourData.append(tmp)
    newOneHourDataPD = pd.DataFrame(newOneHourData, \
                                   columns=['city', 'Year', 'Mon','Day','Hour',\
                                            'weather','temp_c','pressure_mb',\
                                    'relative_humidity','wind_degrees','wind_kph' ])
    beijingHour = datetime.now().strftime('%H')
    newOneHourDataPD.to_csv('/home/yichengkeg/kdd/clean/londonAir_realtime' + '/' +  \
                              date +  beijingHour  + '_me_grid.csv',index=False)

    aqiStationDataPD = pd.DataFrame(aqiStationData, \
                                    columns=['city', 'Year', 'Mon','Day','Hour',\
                                             'weather','temp_c','pressure_mb',\
                                             'relative_humidity','wind_degrees','wind_kph' ])
    aqiStationDataPD.to_csv('/home/yichengkeg/kdd/clean/londonAir' + '/' + date +  '_me_grid.csv',index=False)

def getWeatherToday(filespath, _cityList):
    today = datetime.now().strftime('%Y%m%d')
    data = getWeatherOneDay(filespath, today, _cityList)  

def main():
   helpInfo =  " Use:   \n"
   helpInfo += "     -s   specify one day data processing \n" 
   helpInfo += "          eg. python ./datatranWeath.py  -s 20180123 /home/szw16/kdd/weather/london/data/ \n"
   helpInfo += "     -t   deal today data set \n"
   helpInfo += "          eg. python ./datatranWeath.py  -t today   /home/szw16/kdd/weather/london/data/ \n"
   helpInfo += "     -h   print help info \n"
   
   if len(sys.argv) != 4:
       print(helpInfo) 
       return -1
   date = sys.argv[2]
   path = sys.argv[3]

   if sys.argv[1] == '-t' and len(sys.argv) == 4:
       _data = getWeatherToday(path, _stationList) 

   elif sys.argv[1] == '-s' and len(sys.argv) ==4:
       _data = getWeatherOneDay(path,  date, _stationList)

   else:
       print(helpInfo)
   return 0

if __name__ == "__main__":
    main()

