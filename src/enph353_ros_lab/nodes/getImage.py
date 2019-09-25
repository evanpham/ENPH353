#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
import numpy as np


def findLine(image, height, width):
    # Convert to binary image, and find all black pixels (the line)
    # Only checks bottom 25 rows of pixels
    # Blurring and re-binarying helps remove false black pixels
    bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]
    bw = cv2.blur(bw, (10, 10))
    bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]

    pixels = []
    for x in range(width):
        for y in range(height-25, height):
            if (bw[y, x, :] == [0, 0, 0]).all():
                pixels.append([x, y])
    pixels = np.array(pixels)

    return pixels


def callback(data):
    # Get image dimensions
    h = data.height
    w = data.width

    # Report dimensions to log
    rospy.loginfo("height: %s  width: %s", h, w)

    # Find image matrix
    img = np.fromstring(data.data, dtype='uint8').reshape((h, w, 3))

    # Returns coordinates of the pixels in the line
    pixels = findLine(img, h, w)

    # Get all black pixels in the bottom 100 rows
    pixels = pixels[pixels[:, 1] > h-100]
    xPos = np.mean(pixels[:, 0])

    # Place green circle on center of line at bottom and show the frame
    cv2.circle(img, (int(xPos), int(h-20)), 10, (0, 200, 0), -1)
    cv2.imshow('frame', img)

    # For debugging
    print(img)

    # Show camera feed
    cv2.imshow("frame", img)
    cv2.waitKey(25)
    talker()


def listener():
    # Initialize this ros node
    rospy.init_node('vidFeed', anonymous=True)

    # This node subscribes to the camera image feed
    rospy.Subscriber('/bot/camera1/image_raw', Image, callback)
    rospy.spin()


def talker():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        vel_msg = Twist()
        vel_msg.linear.x = .05
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        rate.sleep()
        pub.publish(vel_msg)


if __name__ == '__main__':
    listener()
