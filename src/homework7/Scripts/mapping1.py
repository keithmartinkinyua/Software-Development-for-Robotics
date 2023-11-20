#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import numpy as np
import cv2 as cv
from math import trunc

mapSize = 1500
canvas = np.zeros((mapSize, mapSize), dtype='uint8')
white = (255, 255, 255)

def map(odom: Odometry):
    coord_x = trunc((round(odom.pose.pose.position.x, 2) * 100) + trunc(mapSize / 2))
    coord_y = trunc((round(odom.pose.pose.position.y, 2) * 100) + trunc(mapSize / 2))
    print('Turtlebot Position: x={x} | y={y}'.format(x=coord_x, y=coord_y))
    # plot the position
    cv.circle(canvas, (coord_x, coord_y), 1, white, -1)
    cv.imshow('Turtlebot3 Map', canvas)
    cv.waitKey(1)

if __name__ == '__main__':
    try:
        rospy.init_node('turtlebot3_path', anonymous=True)
        rospy.Subscriber('/odom', Odometry, map)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass
