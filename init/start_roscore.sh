# !/bin/bash
LOG_FILE=/root/autostart/logs/log_start_roscore.txt
echo "" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "#############################################" >> ${LOG_FILE}
echo "Running start_roscore.sh" >> ${LOG_FILE}
echo $(date) >> ${LOG_FILE}
echo "#############################################" >> ${LOG_FILE}
echo "" >> ${LOG_FILE}
echo "Logs:" >> ${LOG_FILE}

set -e

{

source /root/ros_catkin_ws/install_isolated/setup.bash

sleep 5

} &>> ${LOG_FILE}

set -v

{
if [[ $(hostname -I) == *"192.168.1.127"* ]]; then
  export ROS_IP=192.168.1.127
fi
roscore

} &>> ${LOG_FILE}
