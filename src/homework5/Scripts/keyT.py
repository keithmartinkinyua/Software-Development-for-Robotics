#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty
from turtlesim.msg import Pose
from turtlesim.srv import Spawn


class keyTurtleNode:
    def __init__(self):
        rospy.init_node('keyTurtle_', anonymous=True)
        self.pose = Pose()

    def pose(self, pose):
        self.pose = pose

    def spawn_turtle(x, y, theta):
        rospy.wait_for_service('/spawn')
        try:
            spawn = rospy.ServiceProxy('/spawn', Spawn)
            spawn(x, y, theta,)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
        
    
    def keyTurtleN():
        key_mappings = {
        'w': (1, 0),
        'a': (0, 1),
        's': (-1, 0),
        'd': (0, -1),
        ' ': (0, 0)
        }
        settings = termios.tcgetattr(sys.stdin)

        
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        
        
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            key = key
            
            if key in key_mappings:
                twist = Twist()
                twist.linear.x = key_mappings[key][0]
                twist.angular.z = key_mappings[key][1]
                pub.publish(twist)

            rate.sleep()

#if __name__ == '__main__':
#    try:
#        KeyTurtleNode_ = keyTurtleNode()
#    except rospy.ROSInterruptException:
#        pass
