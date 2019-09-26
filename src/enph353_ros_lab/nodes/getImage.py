#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
import numpy as np


class Robot:

    def __init__(self):
        rospy.init_node('robot', anonymous=True)

        self.camera_subscriber = rospy.Subscriber('/rrbot/camera1/image_raw', Image, self.callback)
        self.vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.error = 0
        self.error_prev = 0
        self.w = 0
        self.h = 0
        self.camera_img = Image()
        self.kp = 0.003
        self.kd = 0.0001

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
        except:
            print("ahhhhhhhh")

        return (cX, cY)

    def callback(self, data):
        # Get image dimensions
        if (self.h, self.w == 0):
            self.h = data.height
            self.w = data.width

        # Find image matrix
        self.camera_img = np.fromstring(data.data, dtype='uint8').reshape((self.h, self.w, 3))

        center = self.getCenter()
        self.error = self.w/2 - center[0]
        cv2.circle(self.camera_img, (self.error, center[1]+250), 10, (255, 255, 0), -1)

        # Display the resulting frame
        cv2.imshow('img', self.camera_img)
        cv2.waitKey(25)

        if (center[0] == -1):
            self.talker(self.error_prev)

        else:
            self.error_prev = center[0]
            self.talker(self.error)

    def listener(self):
        # This node subscribes to the camera image feed
        rospy.spin()

    def talker(self, error):

        derivative = self.error_prev - self.error

        rate = rospy.Rate(10)  # 10hz
        if not rospy.is_shutdown():
            vel_msg = Twist()
            vel_msg.linear.x = .20
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z += error*self.kp + derivative*self.kd
            rate.sleep()
            self.vel_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        print("STARTING")
        bot = Robot()
        bot.listener()
    except rospy.ROSInterruptException:
        pass
