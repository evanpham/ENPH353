#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
# from std_msgs.msg import Float64
import time
import sys
import cv2
import numpy as np


class LineFollower:

    def __init__(self):
        self.cam_path = '/R1/pi_camera/image_raw'
        self.vel_pub = rospy.Publisher('/R1/skid_vel', Twist, queue_size=1)
        self.initial_move()
        self.listener = rospy.Subscriber(self.cam_path, Image, self.callback)
        self.data = None
        self.slice_num = 30
        self.frame = Image()
        self.bridge = CvBridge()

        time.sleep(5)

    def initial_move(self):
        print("first moves")
        self.move("L")
        time.sleep(.5)
        self.move("F")
        time.sleep(.25)
        self.move("L")
        time.sleep(1)
        print("moved")
        self.stop()

    def move(self, action):
        vel_cmd = Twist()
        if action == "F":  # FORWARD
            vel_cmd.linear.x = 0.4
            vel_cmd.linear.y = 0
            vel_cmd.linear.z = 0
            vel_cmd.angular.z = 0.0
        elif action == "L":  # LEFT
            vel_cmd.linear.x = 0.0
            vel_cmd.angular.z = 0.5
        elif action == "R":  # RIGHT
            vel_cmd.linear.x = 0.0
            vel_cmd.angular.z = -0.5
        print(vel_cmd)
        self.vel_pub.publish(vel_cmd)

    def stop(self):
        vel_cmd = Twist()
        vel_cmd.linear.x = 0
        vel_cmd.angular.z = 0

        self.vel_pub.publish(vel_cmd)

    def callback(self, data):
        try:
            self.frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Get image dimensions
        h = data.height
        w = data.width

        # Turn image black and white and slice into thin images
        # Find which slice contains right curb
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        bw = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)[1]
        slices = []*self.slice_num
        state = [0]*self.slice_num
        line_strength = state
        state_num = 0
        max = 0

        for i in range(self.slice_num):
            s = bw[2*h/3:h, i*w/self.slice_num:(i+1)*w/self.slice_num]
            slices.append(s)
            line_strength[i] = np.sum(s)
            if line_strength[i] > max:
                state = [0]*self.slice_num
                state[i] = 1
                state_num = i

        cv2.circle(self.frame, (w*state_num/self.slice_num, h-10), 10, (0, 255, 0), -1)
        print(state_num)
        # cv2.imshow("frame", bw)
        # cv2.waitKey(25)
        self.follow(state_num)

    def follow(self, state):
        if state < 15*self.slice_num/20:
            self.move("L")
        elif state > 18*self.slice_num/20:
            self.move("R")
        else:
            self.move("F")


def main(args):
    rospy.init_node('line_follower', anonymous=True)
    follower = LineFollower()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main(sys.argv)
