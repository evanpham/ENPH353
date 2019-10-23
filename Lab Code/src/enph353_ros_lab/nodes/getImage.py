#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import cv2
import numpy as np




def getCenter(image, width, height):
	global xLast
	global size
	# Crop image
	crop_img = image[height-550:height-250, 0:width]
	# Grayscale
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	# Gaussian blur
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	# Colour thresh
	ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

	#cv2.imshow('crop img', crop_img)
	#cv2.imshow('blur img', blur)


	# Find center
	M = cv2.moments(thresh)
	cX, cY = 0, 0
	try:
		cX = int(M["m10"]/M["m00"])
		cY = int(M["m01"]/M["m00"])
	except:
		print("ahhhhhhhh")
		if xLast > 400:
			side = 1
			cX = 800
		else:
			side = -1
			cX = 0 
		
		

	xLast = cX
	state(cX)

	return (cX, cY)


def callback(data):
	global xLast

	setpoint()

	# Get image dimensions
	h = data.height
	w = data.width

	# Report dimensions to log
	rospy.loginfo("height: %s  width: %s", h, w)

	# Find image matrix
	img = np.fromstring(data.data, dtype='uint8').reshape((h, w, 3))

	center = getCenter(img, w, h)
	cv2.circle(img, (xLast, 450), 10, (255, 255, 0), -1)

	# Display the resulting frame
	#cv2.imshow('img', img)
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

def setpoint():
	#This bit of code continuosly sends our desired state to be 
	#middle of the screen
	setpoint_pub = rospy.Publisher('/setpoint', Float64, queue_size=10)
	setpoint = Float64()
	setpoint.data = 400.0
	setpoint_pub.publish(setpoint)

def state(x):
	#This code will send the current state to pid
	state_pub = rospy.Publisher('/state', Float64, queue_size=10)
	state = Float64()
	state.data = x
	state_pub.publish(state)

def controlEffort(val):
	global effort
	effort = val.data
	print(effort)

def talker(x, width):
	global xLast
	global effort
	
	rospy.Subscriber('control_effort', Float64, controlEffort)

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rate = rospy.Rate(10)  # 10hz
	if not rospy.is_shutdown():
		vel_msg = Twist()
		vel_msg.linear.x = 0.05
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0.01*effort
		rate.sleep()
		pub.publish(vel_msg)

if __name__ == '__main__':
	xLast = 0
	effort = 0
	side = 1
	listener()
