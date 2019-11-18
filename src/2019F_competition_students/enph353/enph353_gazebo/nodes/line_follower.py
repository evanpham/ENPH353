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
        self.listener = rospy.Subscriber(self.cam_path, Image, self.callback)
        self.data = None
        self.lastCross = time.time()
        self.lastCar = time.time()
        self.gettinLicense = False
        self.notKillin = False
        self.initialized = False
        self.slice_num = 30
        self.frame = Image()
        self.bridge = CvBridge()

    def register(self):
        registration = self.team + ',' + self.password + ',0,AB12'
        print(registration)
        self.plate_pub.publish(registration)

    def initial_move(self):
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
        self.initialized = True

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
        elif action == "B":  # BACKWARDS
            vel_cmd.linear.x = -0.2
            vel_cmd.angular.z = 0.0
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

        if not self.initialized:
            self.initial_move()

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

        # if ((time.time()-self.lastCross > 5) and self.atCrosswalk()):
        #     self.notKillin = True
        #     self.stop()
        #     self.lastCross = time.time()
        # elif self.notKillin:
        #     self.dontKillThePedestrian(gray)
        if ((time.time()-self.lastCar > 2) and self.atCar()):
            self.gettinLicense = True
            self.stop()
            self.lastCar = time.time()
        elif self.gettinLicense:
            self.getLicense()
        else:
            self.follow(state_num)

        # cv2.imshow("frame", self.red_filter())
        # cv2.waitKey(25)
        # self.follow(state_num)

    def getLicense(self):
        cv2.imshow("frame", self.frame)
        cv2.waitKey(25)
        if self.getBlueness() > 10000000:
            self.move("B")
        else:
            filename = "../media/cars/" + str(time.time()) + ".png"
            cv2.imwrite(filename, self.frame)
            self.gettinLicense = False
            self.lastCar = time.time()

    def getBlueness(self):
        blue = self.blue_filter()
        return np.sum(blue)

    def atCar(self):
        blueness = self.getBlueness()

        if blueness > 14000000:
            print("atCAR")
            return True
        return False

    def blue_filter(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([110, 125, 30])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        return mask

    def red_filter(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_red = np.array([0,150,0])
        upper_red = np.array([5,255,255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        return mask

    def dontKillThePedestrian(self, image):
        bw = cv2.threshold(image, 225, 255, cv2.THRESH_BINARY)[1]
        corner = bw[300:400, 750:850]
        # cornerG = image[300:400, 750:850]
        # cv2.imshow("dontkill", corner)
        # cv2.imshow("dontkill2", cornerG)
        # cv2.waitKey(25)
        print(np.sum(corner))
        if (np.sum(corner) < 500):
            self.stop()
        else:
            print("ZUM")
            self.notKillin = False
        self.lastCross = time.time()

    def atCrosswalk(self):
        red = self.red_filter()
        h, w = red.shape[0:2]

        for i in range(8, 10):
            s = red[i*h/10, w/4:3*w/4]
            # check how red the slice is
            if np.sum(s) > 10000:
                cv2.circle(red, (w/2, i*h/10), 20, (255, 0, 0), -1)
                print("at cross")
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
