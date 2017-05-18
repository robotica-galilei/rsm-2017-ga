import sys
sys.path.append("../")
import rospy
from std_msgs.msg import String
import time

def callback(data):
     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

if __name__ == '__main__':
   rospy.init_node('listener', anonymous=True)
   rospy.Subscriber("sensors", String, callback)
   time.sleep(10)
