#!/bin/bash
cd /home/orange/kddData/london/crawler/beijing/weatherCaiyun
sh  getWeath.sh
/home/orange/anaconda2/bin/python datatranWeath.py -t  today /home/orange/kddData/london/crawler/beijing/weatherCaiyun/data/
