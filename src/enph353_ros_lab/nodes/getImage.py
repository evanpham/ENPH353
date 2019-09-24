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


if __name__ == '__main__':
    listener()
