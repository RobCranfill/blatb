#!/bin/bash
# This script is invoked by cron to adjust the backlight.

export PYTHONPATH=/home/pi/.local/bin:/home/pi/.local/lib:/home/pi/.local/share
#echo `date` - pythonpath is $PYTHONPATH

cd /home/pi/proj/blatb/

python3 /home/pi/proj/blatb/blatb.py >>/home/pi/proj/blatb/blatb-run.log

