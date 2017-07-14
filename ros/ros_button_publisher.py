import sys
sys.path.append("../")
import rospy
import time
from std_msgs.msg import String
try:
    import sensors.start_button as button
except:
    sys.path.append("/root/rsm-2017-ga/")
    import sensors.start_button as button


def talker():
    pub = rospy.Publisher('button', String, queue_size=1)
    rospy.init_node('button_talker')
    b = button.StartButton()

    while not rospy.is_shutdown():
        val = b.read_raw()
        msg = str(val)
        rospy.loginfo('%s', msg)
        pub.publish(msg)
        time.sleep(0.005)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
