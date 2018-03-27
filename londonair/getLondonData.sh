#!/bin/bash
STARTDATE=`date +"%Y-%m-%d" -d '-8 hour' -d '-1 day'`
ENDDATE=`date +"%Y-%m-%d"  -d '-8 hour' -d '+1 day'`
day=`date +"%Y%m%d"`
mkdir  -p ./data/$day
for SITECODE in $(cat ./siteCode)
do
   curDate=`date +"%Y-%m-%d %H:%M:%S"`

   #info=`curl http://api.erg.kcl.ac.uk/AirQuality/Data/Wide/Site/SiteCode=${SITECODE}/StartDate=${STARTDATE}/EndDate=${ENDDATE}/Json`
   info=`curl http://api.erg.kcl.ac.uk/AirQuality/Data/Site/SiteCode=${SITECODE}/StartDate=${STARTDATE}/EndDate=${ENDDATE}/json`
   echo ${info} >> ./data/$day/${SITECODE}_${day}.log
done
