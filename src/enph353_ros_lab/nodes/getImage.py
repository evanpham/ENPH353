#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import cv2
import numpy as np


class Robot:

    def __init__(self):
        rospy.init_node('robot', anonymous=True)

        self.camera_sub = rospy.Subscriber('/rrbot/camera1/image_raw',
                                           Image, self.callback)
        self.ctrl_sub = rospy.Subscriber('control_effort', Float64, self.ctrlEffort)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.setpt_pub = rospy.Publisher('/setpoint', Float64, queue_size=10)
        self.state_pub = rospy.Publisher('/state', Float64, queue_size=10)
        self.error = 0
        self.error_prev = 0
        self.w = 0
        self.h = 0
        self.camera_img = Image()
        self.state = Float64()
        self.effort = 0
        self.rate = rospy.Rate(10)
        self.setpoint()

    def getCenter(self):
        # Crop image
        crop_img = self.camera_img[self.h-100:self.h, 0:self.w]
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
            print("Line Found")
            print(cX, cY)
        except ZeroDivisionError:
            print("No Line Found")

        self.update_state(cX)
        return (cX, cY)

    def callback(self, data):
        # Get image dimensions
        if (self.h, self.w == 0):
            self.h = data.height
            self.w = data.width

        # Find image matrix
        self.camera_img = np.fromstring(data.data, dtype='uint8').reshape((self.h, self.w, 3))
        center = self.getCenter()
        cv2.circle(self.camera_img,
                   (self.error, center[1]+250), 10, (255, 255, 0), -1)

        # Display the resulting frame
        cv2.imshow('img', self.camera_img)
        cv2.waitKey(25)

        if (center[0] != -1):
            self.error_prev = self.error
            self.error = self.w/2 - center[0]

    def followLine(self):
        while not rospy.is_shutdown():
            self.ctrl_sub
            self.state_pub.publish(self.state)
            vel_msg = Twist()
            vel_msg.linear.x = .05
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z += 0.01*self.effort
            self.vel_pub.publish(vel_msg)
            self.rate.sleep()
            print("spinnin")
            rospy.spin()

    def setpoint(self):
        """ This bit of code continuosly sends our desired state to be 
            in the middle of the screen """
        print("SETTING POINT\n\n\n\n")
        setpoint = Float64()
        setpoint.data = float(self.w/2)
        self.setpt_pub.publish(setpoint)

    def update_state(self, x):
        print("UPDATING STATE\n\n\n\n")
        # This code will send the current state to pid
        if x != -1:
            self.state.data = self.effort
            print(self.state.data)
            self.state_pub.publish(self.state)

    def ctrlEffort(self, val):
        print("CHECKIN CONTROL\n\n\n\n")
        self.effort = val.data


if __name__ == '__main__':
    try:
        print("STARTING")
        bot = Robot()
        bot.followLine()
    except rospy.ROSInterruptException:
        pass
