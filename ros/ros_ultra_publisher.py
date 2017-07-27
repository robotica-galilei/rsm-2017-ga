import sys
sys.path.append("../")
import rospy
import time
from std_msgs.msg import String
try:
    import sensors.ultra as ultra
except:
    sys.path.append("/root/rsm-2017-ga/")
    import sensors.ultra as ultra

def talker():
    pub = rospy.Publisher('ultra', String, queue_size=1)
    rospy.init_node('ultra_talker')
    time_now = time.time()
    u = ultra.Ultra()
    while not rospy.is_shutdown():
        dic = ultra.read_raw()
        msg = dic['NE'] + ':' + dic['NO']
        pub.publish(msg)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
