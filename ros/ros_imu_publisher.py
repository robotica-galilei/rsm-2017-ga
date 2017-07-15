import sys
sys.path.append("../")
import rospy
import time
from std_msgs.msg import String
try:
    import sensors.imu as imu
except:
    sys.path.append("/root/rsm-2017-ga/")
    import sensors.imu as imu

def talker():
    pub = rospy.Publisher('imu', String, queue_size=1)
    rospy.init_node('imu_talker')
    time_now = time.time()
    gyro = imu.Imu()
    while not rospy.is_shutdown():
        gyro.update()
        pub.publish(str(gyro.yaw) + ":" + str(gyro.pitch) + ":" + str(gyro.roll) + ":" + str(gyro.yawsum))
        time.sleep(0.01)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
