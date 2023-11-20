#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10) #Topic name
    rospy.init_node('talker', anonymous=True) # node name, this can be changed during remapping
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "Hey there %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
  
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass