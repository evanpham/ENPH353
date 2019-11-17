#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
# from std_msgs.msg import Float64
import time
import sys
import cv2
import numpy as np
from scipy import stats


class LineFollower:

    def __init__(self):
        self.team = "123"
        self.password = '456'
        self.cam_path = '/R1/pi_camera/image_raw'
        self.vel_pub = rospy.Publisher('/R1/skid_vel', Twist, queue_size=1)
        self.plate_pub = rospy.Publisher('/license_plate', String, queue_size=1)
        self.register()
        self.initial_move()
        self.listener = rospy.Subscriber(self.cam_path, Image, self.callback)
        self.data = None
        self.lastCross = time.time()
        self.slice_num = 30
        self.frame = Image()
        self.bridge = CvBridge()

        time.sleep(5)

    def register(self):
        registration = self.team + ',' + self.password + ',0,AB12'
        print(registration)
        self.plate_pub.publish(registration)

    def initial_move(self):
        print("first moves")
        # self.move("LL")
        # time.sleep(.5)
        # self.move("F")
        # time.sleep(.25)
        # self.move("LL")
        # time.sleep(1)
        # print("moved")
        # self.stop()
        self.move("LL")
        time.sleep(.5)
        self.move("F")
        time.sleep(.5)
        self.move("LL")
        time.sleep(2)
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
            vel_cmd.linear.x = 0.2
            vel_cmd.angular.z = 0.5
        elif action == "R":  # RIGHT
            vel_cmd.linear.x = 0.2
            vel_cmd.angular.z = -0.5
        elif action == "LL":  # LEFT
            vel_cmd.linear.x = 0.0
            vel_cmd.angular.z = 0.5
        elif action == "RR":  # RIGHT
            vel_cmd.linear.x = 0.0
            vel_cmd.angular.z = -0.5
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
        # if (self.atCrosswalk(self.frame) and time.time()-self.lastCross > 5):
        #     self.stop()
        #     self.dontKillThePedestrian(gray)
        # else:
        #     self.follow(state_num)
        # cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow("frame", self.frame)
        cv2.waitKey(25)
        # self.follow(state_num)

    def dontKillThePedestrian(self, image):
        bw = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)[1]
        corner = bw[300:400, 750:850]
        # cornerG = image[300:400, 750:850]
        # cv2.imshow("dontkill", corner)
        # cv2.imshow("dontkill2", cornerG)
        cv2.waitKey(25)
        print(np.sum(corner))
        if (np.sum(corner) < 500):
            self.stop()
        else:
            self.lastCross = time.time()

    def atCrosswalk(self, image):
        h, w = image.shape[0:2]

        for i in range(8, 10):
            s = image[i*h/10, w/4:3*w/4, :]
            # check how red the slice is
            if np.sum(s[:, 2]) > 80000 and np.sum(s[:, 1]) < 80000:
                cv2.circle(image, (w/2, i*h/10), 20, (255, 0, 0), -1)
                return True
        return False

    def follow(self, state):
        if state < 25*self.slice_num/30:
            self.move("LL")
        elif state < 26*self.slice_num/30:
            self.move("L")
        elif state > 28*self.slice_num/30:
            self.move("R")
        elif state > 29*self.slice_num/30:
            self.move("RR")
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
