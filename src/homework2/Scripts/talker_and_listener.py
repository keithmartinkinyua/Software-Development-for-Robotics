#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
# In ROS, nodes are uniquely named. If two nodes with the same
# name are launched, the previous one is kicked off. The
# anonymous=True flag means that rospy will choose a unique
# name for our 'listener' node so that multiple listeners can
# run simultaneously.
    rospy.Subscriber("sub_topic", String, callback)


def talker():
    message_counter = 0
    pub = rospy.Publisher('pub_topic', String, queue_size=10) 
    # queue size refers to the size of the message
    rospy.init_node('talker', anonymous=True)
    node_name = rospy.get_caller_id() #name of the node.
    rate = rospy.Rate(1) # 1hz
    listener()

    while not rospy.is_shutdown():
        the_str = "Our world %s" % rospy.get_time()
        #hello_str = "Our world"
        #rospy.loginfo(the_str)
        message_counter += 1
        message = the_str + " " + node_name + " " + " " + str(message_counter)
        pub.publish(message)
        #print(message)
        rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass