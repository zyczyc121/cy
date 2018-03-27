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

# 获取的城市列表指标# 获取的空气指标
_stationList = ["ab001","ab002","ab003","ab004","ab005","ab006","ab007","ab008","ab009",\
                "ab010","ab011","ab012","ab013","ab014","ab015","ab016","ab017","ab018",\
                "ab019","ab020","ab021","ab022","ab023","ab024","ab025","ab026","ab027",\
                "ab028","ab029","ab030","ab031","ab032","ab033","ab034","ab035","ab036",\
                "ab037","ab038","ab039","ab040","ab041","ab042","ab043","ab044","ab045",\
                "ab046","ab047","ab048","ab049","ab050","ab051","ab052","ab053","ab054",\
                "ab055","ab056","ab057","ab058","ab059","ab060","ab061","ab062","ab063",\
                "ab064","ab065","ab066","ab067","ab068","ab069","ab070","ab071","ab072",\
                "ab073","ab074","ab075","ab076","ab077","ab078","ab079","ab080","ab081",\
                "ab082","ab083","ab084","ab085","ab086","ab087","ab088","ab089","ab090",\
                "ab091","ab092","ab093","ab094","ab095","ab096","ab097","ab098","ab099",\
                "ab100","ab101","ab102","ab105","ab106","ab107","ab108","ab109","ab110",\
                "ab111","ab112","ab113","ab114","ab115","ab116","ab117","ab118","ab119",\
                "ab120","ab121","ab122","ab123","ab124","ab125","ab126","ab127","ab128",\
                "ab129","ab130","ab131","ab132","ab133","ab134","ab135","ab136","ab137",\
                "ab138","ab139","ab140","ab141","ab142","ab143","ab144","ab145","ab146",\
                "ab147","ab148","ab149","ab150","ab151","ab152","ab153","ab154","ab155",\
                "ab156","ab157","ab158","ab159","ab160","ab161","ab162","ab163","ab164",\
                "ab165","ab166","ab167","ab168","ab169","ab170","ab171","ab172","ab173",\
                "ab174","ab175","ab176","ab177","ab178","ab179","ab180","ab181","ab182",\
                "ab183","ab184","ab185","ab186","ab187","ab188","ab189","ab190","ab191",\
                "ab192","ab193","ab194","ab195","ab196","ab197","ab198","ab199","ab200",\
                "ab201","ab202","ab203","ab204","ab205","ab206","ab207","ab208","ab209",\
                "ab210","ab211","ab212","ab213","ab214","ab215","ab216","ab217","ab218",\
                "ab219","ab220","ab221","ab222","ab223","ab224","ab225","ab226","ab227",\
                "ab228","ab229","ab230","ab231","ab232","ab233","ab234","ab235","ab236",\
                "ab237","ab238","ab239","ab240","ab241","ab242","ab243"]
# 或缺指定date的天气
def getWeatherOneDay(filespath, date, _stationList):
    newOneHourData= []
    aqiStationData = []
    for city in _stationList:
        path = filespath + date + '/' + str(city) + '_' + date + '.log' 
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
                              date +  beijingHour  + '_me.csv',index=False)

    aqiStationDataPD = pd.DataFrame(aqiStationData, \
                                    columns=['city', 'Year', 'Mon','Day','Hour',\
                                             'weather','temp_c','pressure_mb',\
                                             'relative_humidity','wind_degrees','wind_kph' ])
    aqiStationDataPD.to_csv('/home/yichengkeg/kdd/clean/londonAir' + '/' + date +  '_me.csv',index=False)

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

