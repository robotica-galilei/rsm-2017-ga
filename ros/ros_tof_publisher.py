import sys
sys.path.append("../")
import rospy
import time
from std_msgs.msg import String
import sensors.tof as tof

def talker():
    pub = rospy.Publisher('sensors', String, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    time_now = time.time()
    directions = ['N', 'S', 'E', 'O']
    rates = {'N': 0.1, 'S': 0.1, 'E': 0.3, 'O': 0.3, 'NE': 0.3, 'NO': 0.3}
    last_read = {'N': time_now, 'S': time_now, 'E': time_now, 'O': time_now}
    t = tof.Tof()
    t.activate_all()
    while not rospy.is_shutdown():
        for direction in directions:
            if time.time()-last_read[direction] > rates[direction]:
                val = str(t.read_fix(direction))
                msg = direction + ':' + val
                rospy.loginfo('Read %s', msg)
                pub.publish(msg)
                last_read[direction] = time.time()
            time.sleep(0.001)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
