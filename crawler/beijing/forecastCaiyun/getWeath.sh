#!/bin/bash
day=`date +"%Y%m%d"`
mkdir  -p ./data/$day
for st  in $(cat ./stationId)
do 
    curDate=`date +"%Y-%m-%d %H:%M:%S"`
    staName=`echo $st|awk -F, '{print $1}'`
    curtime=`date +"%s"`
    lat=`echo $st|awk -F, '{print $2}'`
    lng=`echo $st|awk -F, '{print $3}'`
    info=`curl https://api.caiyunapp.com/v2/YiMxfNNg1XXxSf9x/${lng},${lat}/weather?begin=${curtime}&tzshift=0&hourlysteps=72`
    echo $info |grep  -i ok >/dev/null
    if [ $? -ne 0 ]
    then
       echo "$curDate ${staName}  is fail"
    else
        echo $info >> ./data/$day/${staName}_${day}.log
    fi
done
