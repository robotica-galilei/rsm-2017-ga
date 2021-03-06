# !/bin/bash
LOG_FILE=/root/autostart/logs/log_autostart_screens.txt

echo "" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "#############################################" >> ${LOG_FILE}
echo "Running autostart_screens.sh" >> ${LOG_FILE}
echo $(date) >> ${LOG_FILE}
echo "#############################################" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "Logs:" >> ${LOG_FILE}

set -e
set -v

{
source /root/ros_catkin_ws/install_isolated/setup.bash

if [[ $(hostname -I) == *"192.168.7.2"* ]]; then
  export ROS_MASTER_URI=http://192.168.7.2:11311
  export ROS_IP=192.168.7.2
fi

if [[ $(hostname -I) == *"192.168.1.127"* ]]; then
  export ROS_MASTER_URI=http://192.168.1.127:11311
  export ROS_IP=192.168.1.127
fi


sh /root/rsm-2017-ga/start_routine.sh
#screen -d -m bash /root/rsm-2017-ga/start.sh
screen -d -m bash /root/rsm-2017-ga/init/start_roscore.sh
sleep 7 #Give roscore some time to startup
screen -d -m bash -c "while true; do python /root/rsm-2017-ga/ros/ros_tof_publisher.py; sleep 1; done"
screen -d -m bash -c "while true; do python /root/rsm-2017-ga/ros/ros_temp_col_publisher.py; sleep 1; done"
screen -d -m bash -c "while true; do python /root/rsm-2017-ga/ros/ros_button_publisher.py; sleep 1; done"
screen -d -m bash -c "while true; do python /root/rsm-2017-ga/ros/ros_imu_publisher.py; sleep 1; done"
screen -L -d -m bash -c "while true; do python /root/rsm-2017-ga/parti_ti_prego.py; sleep 1; done"

} &>> ${LOG_FILE}
