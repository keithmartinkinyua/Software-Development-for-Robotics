#!/usr/bin/env python3
import rospy
#from std_msgs.msg import String
from begginer_tutorials.msg import Num
from begginer_tutorials.srv import AddTwoInts,AddTwoIntsResponse
import sys


all_messages = []

def callback(data):
    global all_messages
    all_messages.append(data)
    callback_msg = ""

    for a_message in all_messages:
        callback_msg += a_message.msg + ""
        
    rospy.loginfo(callback_msg)


def handle_add_two_ints(value):
    print("Returning [%s  %s  %s = %s]"%(value.x, value.arithimetic_operator, value.y,(eval(f"{value.x} {value.arithimetic_operator} {value.y}"))))
    result = eval(f"{value.x} {value.arithimetic_operator} {value.y}")
    with_param_factor = result * float(rospy.get_param("/factor"))
    rospy.set_param("/factor", result)
    current_time = rospy.get_time()
    service_name = rospy.get_name() # returns the name of the service
    client = rospy.get_caller_id() #returns the name of the node requestring the service.
    return AddTwoIntsResponse(result, with_param_factor, service_name, client, (rospy.Time.now() - value.timestamp))


def talker(neighboring_node, service_name= "the_service"):
    global all_messages
    message_counter = 0

    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('pub_topic"', Num, queue_size=10) # queue size refers to the size of the message
    rospy.Subscriber('sub_topic', Num, callback,callback_args=pub,queue_size=1) # recieving the messages from the topics that the node is subscribed to


    node_name = rospy.get_caller_id() #name of the node.
    rate = rospy.Rate(1) # 1hz

    
    #my_param = rospy.get_param('/my_parameter') #updating the parameter 
    rospy.Service(service_name, AddTwoInts, handle_add_two_ints)
    


    while not rospy.is_shutdown():
        time_stamp = rospy.get_time()

        the_str = "Our world" 
        message_counter += 1
        message = the_str + " " + node_name + " " + str(message_counter) + " " + str(time_stamp)
        
        to_be_pub = Num()
        to_be_pub.msg = message #creating our custom message.
        pub.publish(to_be_pub)

        all_messages.append(to_be_pub) #putting all the messages together
        for i in all_messages:
            curr_time = rospy.get_time()
            time_diff = float(curr_time - time_stamp)

            if time_diff > 5.0: # ensuring the time difference is not greater than 5.
               all_messages.remove(i)
            else:
               pass
                

        #Logic to publish every single message that meets the criteria
        for j in all_messages:
           pub.publish(j)

        rate.sleep()


  
if __name__ == '__main__':
    try:
        node = rospy.get_param('/node_name')
        friend_node = rospy.get_param('/friend_node_name')
        service_name_ = rospy.get_param('/service_name')
        factor = float(rospy.get_param('/factor'))
        talker(friend_node, service_name_)

    
    except rospy.ROSInterruptException:
        pass

