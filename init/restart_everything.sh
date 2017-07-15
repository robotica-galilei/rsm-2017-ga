# !/bin/bash
killall -9 python
killall -9 screen
screen -wipe

sleep 5

sh /root/rsm-2017-ga/init/autostart_screens.sh
