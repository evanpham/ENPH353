#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np


def callback(data):
    rospy.loginfo("  height: %s  width: %s", data.height, data.width)
    image = np.fromstring(data.data, dtype='uint8').reshape((data.height, data.width, 3))
    print(image)
    cv2.imshow("frame", image)
    cv2.waitKey(25)


def listener():
    rospy.init_node('vidFeed', anonymous=True)

    sub = rospy.Subscriber('/bot/camera1/image_raw', Image, callback)

    rospy.spin()

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
	


if __name__ == '__main__':
    listener()
