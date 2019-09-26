#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
import numpy as np

global xLast = 0


def getCenter(image, width, height):
	# Crop image
	crop_img = image[height-100:height, 0:width]
	# Grayscale
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	# Gaussian blur
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	# Colour thresh
	ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

	# Find center
	M = cv2.moments(thresh)
	cX, cY = -1, -1
	try:
		cX = int(M["m10"]/M["m00"])
		cY = int(M["m01"]/M["m00"])
	except:
		print("ahhhhhhhh")

	return (cX, cY)


def callback(data):
	# Get image dimensions
	h = data.height
	w = data.width

	# Report dimensions to log
	rospy.loginfo("height: %s  width: %s", h, w)

	# Find image matrix
	img = np.fromstring(data.data, dtype='uint8').reshape((h, w, 3))

	center = getCenter(img, w, h)
	cv2.circle(img, (xLast, center[1]+250), 10, (255, 255, 0), -1)

	# Display the resulting frame
	cv2.imshow('img', img)
	cv2.waitKey(25)

	if (center[0] == -1):
		talker(xLast, w)

	else:
		xLast = center[0]
		talker(xLast, w)


def listener():
	# Initialize this ros node
	rospy.init_node('vidFeed', anonymous=True)

	# This node subscribes to the camera image feed
	rospy.Subscriber('/rrbot/camera1/image_raw', Image, callback)
	rospy.spin()


def talker(x, width):

	kp = 0.005
	kd = 0.002
	derivative = xLast - x

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rate = rospy.Rate(10)  # 10hz
	if not rospy.is_shutdown():
		vel_msg = Twist()
		vel_msg.linear.x = .20
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z += (width/2-x)*kp + derivative*kd
		rate.sleep()
		pub.publish(vel_msg)

if __name__ == '__main__':
	listener()
