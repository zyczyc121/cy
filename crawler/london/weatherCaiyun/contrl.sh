#!/bin/bash
cd /home/orange/kddData/london/weatherCaiyun
sh  getWeath.sh
/home/orange/anaconda2/bin/python datatranWeath.py -t  today /home/orange/kddData/london/weaHeyun/data/
