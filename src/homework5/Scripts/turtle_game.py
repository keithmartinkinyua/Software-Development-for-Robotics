#!/usr/bin/env python3

import rospy
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill
from joyT import JoyTurtlesimNode #calling the joy turtle Node from the joy script
from keyT1 import Keyboard_TurtlesimNode #calling the key turtle Node from the joy script

#joy_turtle_score= 0
#key_turtle_score = 0

# create an instance of a turtle.
class TurtleController:
    def __init__(self, turtle_name):
        rospy.init_node(turtle_name)
        self.turtle_name = turtle_name
        self.publisher = rospy.Publisher('/' + turtle_name + '/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/' + turtle_name + '/pose', Pose, self.pose_callback)
        self.pose = Pose()

    def pose_callback(self, pose):
        self.pose = pose

    def move(self, linear_velocity, angular_velocity):
        msg = Twist()
        msg.linear.x = linear_velocity
        msg.angular.z = angular_velocity
        self.publisher.publish(msg)



def spawn_turtle(x, y, theta, name):
    rospy.wait_for_service('/spawn')
    try:
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        spawn(x, y, theta, name)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

 
# randomly generate velocities to move the target and enemy turtle.
def move_randomly(turtle_controller):
    linear = random.uniform(0.1, 1.0)
    angular = random.uniform(0.1, 1.0)
    turtle_controller.move(linear, angular)


# Initializing a node to perform scoring.
def game_scoring(joyTurtle, keyTurtle, enemyTurtle, targetTurtle):
    # calculate joy turtle score when its in the same position as target
    #rospy.init_node('gamemgmt_node')
    global key_turtle_score, joy_turtle_score
    joy_turtle_score= 0
    key_turtle_score = 0


    #Condition for joy turtle getting to the target turtle
    if joyTurtle.pose.x and joyTurtle.pose.y == targetTurtle.pose.x and targetTurtle.pose.y:
        joy_turtle_score +=1 #add a point to the turtle
        print(joy_turtle_score)
        rospy.wait_for_service('/kill')
        killer = rospy.ServiceProxy('/kill', Kill) #initialize killing service
        try:
            killer(targetTurtle)
        except rospy.ServiceException as e:
            rospy.logerr("Unable to kill turtle", e)


    #Condition for key turtle getting to the target turtle
    if keyTurtle.pose.x and keyTurtle.pose.y == targetTurtle.pose.x and targetTurtle.pose.y:
        key_turtle_score +=1 #add a point to the turtle
        print(key_turtle_score)
        rospy.wait_for_service('/kill')
        killer = rospy.ServiceProxy('/kill', Kill) #initialize killing service
        try:
            killer(targetTurtle)
        except rospy.ServiceException as e:
            rospy.logerr("Unable to kill turtle", e)


    # calculate joy turtle score when its in the same position as enemy
    if joyTurtle.pose.x and joyTurtle.pose.y == enemyTurtle.pose.x and enemyTurtle.pose.y:
        joy_turtle_score -=1
        print(joy_turtle_score)


    # calculate Key turtle score when its in the same position as enemy
    if keyTurtle.pose.x and keyTurtle.pose.y == enemyTurtle.pose.x and enemyTurtle.pose.y:
        key_turtle_score -=1
        print(key_turtle_score)
        

    else:
        joy_turtle_score+=0
        print(joy_turtle_score)


    return joy_turtle_score, key_turtle_score



def main_func():
    #original positions of turtles being defined.
    joyTurtle = JoyTurtlesimNode()        #.spawn_turtle(4, 1, 0, 'joyTurtle')
    keyTurtle = Keyboard_TurtlesimNode()  #.spawn_turtle(3, 6, 0, 'keyTurtle_')

    #joyTurtle.spawn_turtle(4, 9, 0, 'JoyTurtle')
    #keyTurtle.spawn_turtle(3, 4, 5, 'keyTurtle')
    #spawn_turtle(2, 9, 0, 'targetTurtle')
    #spawn_turtle(7, 3, 0, 'enemyTurtle')

    global enemyTurtle, targetTurtle
    #joyTurtle = JoyTurtlesimNode()
    #keyTurtle_ = Keyboard_TurtlesimNode()
    targetTurtle = TurtleController('targetTurtle')
    enemyTurtle = TurtleController('enemyTurtle')

    game_scoring(joyTurtle, keyTurtle, enemyTurtle, targetTurtle)


    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        
        # Logging the turtle's position
        #rospy.loginfo("Turtle %s - X: %s, Y: %s", joyTurtle.turtle_name, joyTurtle.pose.x, joyTurtle.pose.y)
        #rospy.loginfo("Turtle %s - X: %s, Y: %s", keyTurtle.turtle_name, keyTurtle.pose.x, keyTurtle.pose.y)
        #rospy.loginfo("Turtle %s - X: %s, Y: %s", targetTurtle.turtle_name, targetTurtle.pose.x, targetTurtle.pose.y)
        #rospy.loginfo("Turtle %s - X: %s, Y: %s", enemyTurtle.turtle_name, enemyTurtle.pose.x, enemyTurtle.pose.y)

        
        rate.sleep()

if __name__ == '__main__':
    main_func()    