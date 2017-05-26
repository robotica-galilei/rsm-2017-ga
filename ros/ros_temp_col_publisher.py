import sys
sys.path.append("../")
import rospy
import time
from std_msgs.msg import String
try:
    import sensors.heat as heat
    import sensors.color as color
except:
    sys.path.append("/root/rsm-2017-ga/")
    import sensors.heat as heat
    import sensors.color as color


def talker():
    pub_heat = rospy.Publisher('heat', String, queue_size=1)
    pub_color = rospy.Publisher('color', String, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    time_now = time.time()
    directions = ['N', 'E', 'O']
    rates = {'N': 0.1, 'E': 0.3, 'O': 0.3, 'COLOR': 0.3}
    last_read = {'N': time_now, 'E': time_now, 'O': time_now, 'COLOR': time_now}
    h = heat.Heat()
    col = color.Color()

    while not rospy.is_shutdown():
        for direction in directions:
            if time.time()-last_read[direction] > rates[direction]:
                val = str(h.read_raw(direction))
                msg = direction + ':' + val
                rospy.loginfo('Read %s', msg)
                pub_heat.publish(msg)
                last_read[direction] = time.time()
            time.sleep(0.001)
        direction = 'COLOR'
        if time.time()-last_read[direction] > rates[direction]:
            val = col.read_raw()
            msg = str(str(val[0]) + ',' + str(val[1]) + ',' + str(val[2]) + ',' + str(val[3]))
            rospy.loginfo('%s', msg)
            pub_color.publish(msg)
            last_read[direction] = time.time()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
