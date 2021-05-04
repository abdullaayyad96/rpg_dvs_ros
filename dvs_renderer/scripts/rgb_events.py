#!/usr/bin/env python2
from dvs_msgs.msg import Event, EventArray
import numpy as np
import rospy

class rgbDivider:
    def __init__(self): 

        self.ros_node = rospy.init_node('tactile_sensor', anonymous=True)       

        self.events_subs = rospy.Subscriber("/dvs/events", EventArray, self.event_callback, queue_size=1)
        self.green_events_pub_1 = rospy.Publisher('/green_events_1', EventArray, queue_size=1)
        self.green_events_pub_2 = rospy.Publisher('/green_events_2', EventArray, queue_size=1)
        self.red_events_pub = rospy.Publisher('/red_events', EventArray, queue_size=1)
        self.blue_events_pub = rospy.Publisher('/blue_events', EventArray, queue_size=1)

        self.green_events_1_queue = []
        self.green_events_2_queue = []
        self.red_events_queue = []
        self.blue_events_queue = []

        self.output_events_msg = EventArray()

        rospy.spin()

    
    def event_callback(self, event_msg):
        self.output_events_msg.header = event_msg.header
        self.output_events_msg.height = event_msg.height
        self.output_events_msg.width = event_msg.width

        self.determine_event_color(event_msg.events)

        #publish green 1
        self.output_events_msg.events = self.green_events_1_queue
        self.green_events_pub_1.publish(self.output_events_msg)
        #publish green 2
        self.output_events_msg.events = self.green_events_2_queue
        self.green_events_pub_2.publish(self.output_events_msg)
        #publish red
        self.output_events_msg.events = self.red_events_queue
        self.red_events_pub.publish(self.output_events_msg)
        #publish blue
        self.output_events_msg.events = self.blue_events_queue
        self.blue_events_pub.publish(self.output_events_msg)

        #clear queues
        self.green_events_1_queue = []
        self.green_events_2_queue = []
        self.red_events_queue = []
        self.blue_events_queue = []


    def determine_event_color(self, event_stream):
        for event in event_stream:
            if ((event.x%2==0) and (event.y%2==0)):
                #Green events 1
                self.green_events_1_queue.append(event)
            elif ((event.x%2==1) and (event.y%2==1)):
                #Green events 2
                self.green_events_2_queue.append(event)        
            elif ((event.x%2==0) and (event.y%2==1)):
                #Red event
                self.red_events_queue.append(event)
            else:
                self.blue_events_queue.append(event)

if __name__ == '__main__':
    robot = rgbDivider()
    exit()

        
