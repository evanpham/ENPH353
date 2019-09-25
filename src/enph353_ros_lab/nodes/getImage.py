#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np


def findLine(image):
    # Convert to binary image, and find all black pixels (the line)
    # Blurring and re-binarying helps remove false black pixels
    bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]
    bw = cv2.blur(bw, (10, 10))
    bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]
    pixels = np.argwhere(bw == 0)

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
    pixels = findLine(img)

    # Get all black pixels in the bottom 100 rows
    pixels = pixels[pixels[:, 1] < 100]
    xPos = np.mean(pixels[:, 0])
    yPos = np.mean(pixels[:, 1])

    # Place green circle on center of line at bottom and show the frame
    cv2.circle(img, (int(w-xPos), int(h-yPos)), 10, (0, 200, 0), -1)

    # For debugging
    print(img)

    # Show camera feed
    cv2.imshow("frame", img)
    cv2.waitKey(25)


def listener():
    # Initialize this ros node
    rospy.init_node('vidFeed', anonymous=True)

    # This node subscribes to the camera image feed
    rospy.Subscriber('/bot/camera1/image_raw', Image, callback)
    rospy.spin()

# def talker():
#     pub = rospy.Publisher('chatter', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     while not rospy.is_shutdown():
#         hello_str = "hello world %s" % rospy.get_time()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()


if __name__ == '__main__':
    listener()
