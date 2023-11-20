#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty
from turtlesim.msg import Pose
from turtlesim.srv import Spawn



class Keyboard_TurtlesimNode:
    def __init__(self):
        global vel_pub
        #rospy.init_node('keyTurtle')
        # set the topic to publish Twist messages to
        vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose = Pose()

    def pose(self, pose):
        self.pose = pose


    def spawn_turtle(x, y, theta, name):
        rospy.wait_for_service('/spawn')
        try:
            spawn = rospy.ServiceProxy('/spawn', Spawn)
            spawn(x, y, theta, name)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)


    def keyTurtle_main():
        # set the rate of the loop
        rate = rospy.Rate(10)

        # initialize the Twist message
        vel_msg = Twist()

        # set the default linear and angular velocities
        linear_speed = 1
        angular_speed = 1

        # initialize keyboard input settings
        tty.setraw(sys.stdin.fileno())
        settings = termios.tcgetattr(sys.stdin)

        # print instructions
        print("Use arrow keys to move the turtle, 'q' to quit")

        # loop to listen to keyboard input
        while not rospy.is_shutdown():
            # get the key input
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
            else:
                key = ''

            # set the linear and angular velocities based on the key input
            if key == 'q':
                break
            elif key == 'A':
                vel_msg.linear.x = linear_speed
                vel_msg.angular.z = 0
            elif key == 'B':
                vel_msg.linear.x = -linear_speed
                vel_msg.angular.z = 0
            elif key == 'C':
                vel_msg.linear.x = 0
                vel_msg.angular.z = -angular_speed
            elif key == 'D':
                vel_msg.linear.x = 0
                vel_msg.angular.z = angular_speed
            else:
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0

            # publish the Twist message
            vel_pub.publish(vel_msg)
            

            # sleep for the loop rate
            rate.sleep()

        # reset the keyboard input settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

#if __name__ == '__main__':
#    try:
#        Keyboard_TurtlesimNode()
#    except rospy.ROSInterruptException:
#        pass
