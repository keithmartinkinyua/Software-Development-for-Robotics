#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn


class JoyTurtlesimNode:
    def __init__(self):
        rospy.init_node('joyTurtle')
        self.cmd_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.pose = Pose()

    def joy_callback(self, joy_msg):
        twist = Twist()
        twist.linear.x = 2 * joy_msg.axes[1] #move forward and back
        twist.angular.z = 2 * joy_msg.axes[0] #move left and right

        #publish turtle commands
        self.cmd_vel_pub.publish(twist)

    def pose(self, pose):
        self.pose = pose

    def spawn_turtle(x, y, theta, name):
        rospy.wait_for_service('/spawn')
        try:
            spawn = rospy.ServiceProxy('/spawn', Spawn)
            spawn(x, y, theta, name)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)


if __name__ == '__main__':
    try:
        joyTurtleNode = JoyTurtlesimNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
