#!/usr/bin/env python3
from __future__ import print_function
from begginer_tutorials.srv import AddTwoInts,AddTwoIntsResponse
import rospy
import sys
import time



def service_name(srvc_name_):
    if srvc_name_ != "":
        s = input(f"Enter the name of the service '{srvc_name_}' (y/n): ")
        if s.lower() == "y":
            return srvc_name_
    srvc_name_ = input("Enter the name of the service:")
    return srvc_name_


def client_side(srvc_name_=""):
    rospy.init_node("client_side", anonymous=False)

    while not rospy.is_shutdown():
        srvc_name__ = service_name(srvc_name_)
        rospy.wait_for_service(srvc_name__)

        try:
            p = rospy.ServiceProxy(srvc_name__, AddTwoInts)
            first_num = float(input("Enter a number:"))
            second_num = float(input("Enter a number:"))
            operation = (input("Enter an operand"))
            factor = float(rospy.get_param('/factor'))

            m = p(first_num, second_num, operation, rospy.Time.now())
            # print("\n - Current Global factor: %s\n"%(factor))
            # print("\n - service: %s, client name ; %s \n response time: %s seconds \n"% (m.my_service_name, m.client_name,(m.network_time.to_sec())))
            print("Outcome is as follows: %s %s %s = %s \n"%(first_num,operation, second_num, m.outcome))

        except rospy.ServiceException as e:
            print("The service failed: %s"%e)
            return
        time.sleep(1)


if __name__ == "__main__":
    client_side()
    

