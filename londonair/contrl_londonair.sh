#!/bin/bash
cd /home/orange/kddData/london/londonair
sh getLondonData.sh
/home/orange/anaconda2/bin/python getCleanData.py -t today /home/orange/kddData/london/londonair/data/
