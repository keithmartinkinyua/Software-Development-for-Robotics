#!/usr/bin/env python3

import rospy
#from std_msgs.msg import String
from begginer_tutorials.msg import Num
all_messages = []
def callback(data):
	global all_messages
	all_messages.append(data)
	callback_msg = ""
	for a_message in all_messages:
		callback_msg += a_message.msg + ""
		rospy.loginfo(callback_msg)
def talker():
	global all_messages
	message_counter = 0
	pub = rospy.Publisher('pub_topic', Num, queue_size=10) 
	
	# queue size refers to the size of the message
	rospy.init_node('talker', anonymous=True)
	node_name = rospy.get_caller_id() #name of the node.
	rate = rospy.Rate(1) # 1hz
	rospy.Subscriber("sub_topic", Num, callback) 
	
	# recieving the messages from the topics that the node is subscribed to
	while not rospy.is_shutdown():
		time_stamp = rospy.get_time()
		the_str = "Our world"
		message_counter += 1
		message = the_str + " " + node_name + " " + str(message_counter) + " " + str(time_stamp)
		
		to_be_pub = Num()
		to_be_pub.msg = message #creating our custom message.
		pub.publish(to_be_pub)#all_messages.append(to_be_pub) #putting all the messages together
		
		for i in all_messages:
			curr_time = rospy.get_time()
			time_diff = float(curr_time - time_stamp)
			if time_diff > 5.0: 
				# ensuring the time difference is not greater than 5.
				all_messages.remove(i)
			else:
				pass
			# Logic to publish every single message that meets the criteria
			for j in all_messages:
				pub.publish(j)
			rate.sleep()
if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
