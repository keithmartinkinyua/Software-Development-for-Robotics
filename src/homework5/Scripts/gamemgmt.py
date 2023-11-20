#!/usr/bin/env python3

import rospy
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill


scores = 0 
normal_turtle_score = 0
target_turtle_score = 0

def turtle_postion(self, turtle_name):
    self.pose = Pose()
    x = Pose.x
    y = Pose.y
    theta = Pose.theta
    return x, y, theta

def game_scoring(normal_turtle, target_turtle, enemy_turtle):
    if turtle_postion(normal_turtle) == turtle_postion(target_turtle):
        normal_turtle_score +=1 #add a point to the turtle
        print(normal_turtle_score)
        rospy.wait_for_service('/kill')
        killer = rospy.ServiceProxy('/kill', Kill) #initialize killing service
        try:
            killer(target_turtle)
        except rospy.ServiceException as e:
            rospy.logerr("Unable to kill turtle", e)

    elif turtle_postion(normal_turtle) == turtle_postion(enemy_turtle):
        normal_turtle_score -=1
    else:
        normal_turtle_score+=0

#if __name__ == "__main__":
    #game_scoring()
    




