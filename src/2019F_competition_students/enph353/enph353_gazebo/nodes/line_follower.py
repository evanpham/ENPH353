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


class LineFollower:

    def __init__(self):
        self.teamAndPass = "123,456"
        self.cam_path = '/R1/pi_camera/image_raw'
        self.vel_pub = rospy.Publisher('/R1/cmd_vel', Twist, queue_size=1)
        self.plate_pub = rospy.Publisher('/license_plate', String, queue_size=1)
        self.car_pub = rospy.Publisher("/car_pics", Image, queue_size=1)
        self.listener = rospy.Subscriber(self.cam_path, Image, self.callback)
        self.data = None
        self.h = 0
        self.w = 0
        self.car_pic_count = 0
        self.plateCount = 0
        self.firstLine = False
        self.pastCar = False
        self.lastCross = rospy.get_rostime().secs
        self.lastCar = rospy.get_rostime().secs
        self.gettinLicense = False
        self.notKillin = False
        self.initialized = False
        self.innerRing = False
        self.innerInit = False
        self.truckPassed = False
        self.slice_num = 30
        self.frame = Image()
        self.last = Image()
        self.bw = Image()
        self.hsv = Image()
        self.bridge = CvBridge()

    def register(self):
        registration = self.teamAndPass + ',0,AB12'
        print(registration)
        self.plate_pub.publish(String(registration))

    def initial_move(self):
        if np.sum(self.bw[8*self.h/10:9*self.h/10, :]) < 5000000:
            self.move("F")
        else:
            self.move("L")
            rospy.sleep(.5)
            print("moved")
            self.stop()
            self.register()
            self.initialized = True

    def inner_initial_moves(self):
        if not self.truckPassed and self.truck_check():
            self.stop()
        elif not self.truckPassed:
            self.truckPassed = True
        elif self.truckPassed and np.sum(self.bw[8*self.h/10:9*self.h/10, :]) < 5000000:
            self.move("F")
        else:
            print("WE HERE")
            self.move("L")
            rospy.sleep(.5)
            self.stop()
            self.innerInit = True

    def truck_check(self):
        change = self.frame[0:2*self.h/3] - self.last[0:2*self.h/3]
        change = cv2.medianBlur(change, 9)
        gray = cv2.cvtColor(change, cv2.COLOR_BGR2GRAY)
        bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]
        bw = cv2.medianBlur(bw, 13)
        boxCount = self.roi(bw)
        
        return boxCount > 0

    def get_state_inner(self):
        road = self.road_filter()[2*self.h/3:-1, :]

        m = cv2.moments(road, True)
        # calculate x,y coordinate of center
        try:
            cX = int(m["m10"] / m["m00"])
            cY = int(m["m01"] / m["m00"])
            
            # put text and highlight the center
            cv2.circle(self.frame, (cX, self.h/2), 5, (0, 255, 255), -1)
        except:
            print("NAH")
        cv2.imshow(".", self.frame)
        cv2.waitKey(25)
        return cX


    def move(self, action):
        vel_cmd = Twist()
        if action == "F":  # FORWARD
            vel_cmd.linear.x = 0.4
            vel_cmd.angular.z = 0.0
        elif action == "L":  # LEFT
            vel_cmd.linear.x = 0.0
            vel_cmd.angular.z = 0.5
        elif action == "R":  # RIGHT
            vel_cmd.linear.x = 0.0
            vel_cmd.angular.z = -0.5
        elif action == "B":  # BACKWARDS
            vel_cmd.linear.x = -0.4
            vel_cmd.angular.z = 0.0
        self.vel_pub.publish(vel_cmd)

    def stop(self):
        vel_cmd = Twist()
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.z = 0.0
        self.vel_pub.publish(vel_cmd)

    def callback(self, data):
        self.data = data
        try:
            self.frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Turn image black and white and get hsv version for color filtering
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.bw = cv2.threshold(gray, 215, 255, cv2.THRESH_BINARY)[1]
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # If the camera is running working and the car hasnt moved, make initial moves
        if (not self.initialized and np.sum(self.bw) > 10000000):
            # Get image dimensions
            self.h = data.height
            self.w = data.width

            # Pull out of parking spot and turn to face road
            self.initial_move()
        # If at inner ring and not initialized run initial inner ring procedure
        elif self.innerRing and not self.innerInit:
            self.inner_initial_moves()
        elif self.innerInit:
            self.gogogoInner()
        elif self.initialized and self.plateCount < 6:
            # Follow road, avoid pedestrians, mark cars
            self.gogogoInner()
        elif self.initialized and self.plateCount >= 6:
            if self.getBlueness() > 500000 and not self.pastCar:  # Get past car
                self.gogogo()
                print(self.getBlueness())
            else:
                self.pastCar = True
                self.getToInnerRing()
        self.last = self.frame

    def gogogoInner(self):
        state = self.get_state_inner()
        if state > self.w/2 + 20:
            self.move("R")
        elif state < self.w/2 - 20:
            self.move("L")
        else:
            self.move("F")

    def getToInnerRing(self):
        if np.sum(self.line_filter()[9*self.h/10:-1, self.w/2-50:self.w/2+50]) < 100:
            # Slice bw image into slices and find out where right curb is
            state_num = 0
            max = 0

            for i in range(self.slice_num-1,-1, -1):
                s = self.bw[8*self.h/10:9*self.h/10, i*self.w/self.slice_num:(i+1)*self.w/self.slice_num]
                if np.sum(s) > max:
                    state_num = i

            self.follow(state_num, "L")
        elif not self.firstLine:
            self.move("F")
            rospy.sleep(.2)
            self.firstLine = True
            print("firstline")
        else:
            self.move("L")
            rospy.sleep(.1)
            self.innerRing = True

    def gogogo(self):
        # Slice bw image into slices and find out where right curb is
        state_num = 0
        max = 0

        for i in range(self.slice_num):
            s = self.bw[2*self.h/3:7*self.h/9, i*self.w/self.slice_num:(i+1)*self.w/self.slice_num]
            if np.sum(s) > max:
                state_num = i

        # If at a crosswalk, stop and set notKillin boolean true
        if ((rospy.get_rostime().secs-self.lastCross > 5) and self.atCrosswalk()):
            self.notKillin = True
            self.stop()
            self.lastCross = rospy.get_rostime().secs
        # If notKillin, dont kill
        elif self.notKillin:
            self.dontKillThePedestrian()
        # If at a car, stop and set gettinLicense boolean true
        elif ((rospy.get_rostime().secs-self.lastCar > 5) and self.atCar()):
            self.gettinLicense = True
            self.lastCar = rospy.get_rostime().secs
        # If gettinLicense, get license
        elif self.gettinLicense:
            self.getLicense()
        # Otherwise, follow the line my dude
        else:
            self.follow(state_num)

    def getLicense(self):
        if self.car_pic_count < 5:
            # filename = "../media/cars/" + str(time.time()) + ".png"
            # cv2.imwrite(filename, self.frame)
            self.move("L")
            rospy.sleep(0.02)
            self.stop()
            rospy.sleep(0.1)
            self.car_pub.publish(self.data)
            self.car_pic_count = self.car_pic_count + 1
        else:
            self.gettinLicense = False
            self.lastCar = rospy.get_rostime().secs
            self.car_pic_count = 0
            self.plateCount = self.plateCount + 1

    def getBlueness(self):
        blue = self.blue_filter()
        return np.sum(blue)

    def atCar(self):
        blueness = self.getBlueness()

        if blueness > 6000000:
            return True
        return False

    def blue_filter(self):
        # define range of blue color in HSV
        lower_blue = np.array([110, 125, 30])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(self.hsv, lower_blue, upper_blue)

        return mask

    def road_filter(self):
        # define range of road color in HSV
        lower_blue = np.array([0, 0, 0])
        upper_blue = np.array([30, 255, 255])
        mask = cv2.inRange(self.hsv, lower_blue, upper_blue)

        return mask

    def red_filter(self):
        # define range of blue color in HSV
        lower_red = np.array([0, 150, 0])
        upper_red = np.array([5, 255, 255])
        mask = cv2.inRange(self.hsv, lower_red, upper_red)

        return mask

    def line_filter(self):
        # define range of line color in HSV
        lower_red = np.array([60, 0, 0])
        upper_red = np.array([80, 255, 255])
        mask = cv2.inRange(self.hsv, lower_red, upper_red)

        return mask

    def roi(self, image):
        boxCount = 0
        kernel = np.ones((1,1), np.uint8) 
        img_dilation = cv2.dilate(image, kernel, iterations=1) 
        cv2MajorVersion = cv2.__version__.split(".")[0]

        # check for contours on thresh
        if int(cv2MajorVersion) >= 4:
            ctrs, hier = cv2.findContours(img_dilation.copy(),
                                          cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
        else:
            im2, ctrs, hier = cv2.findContours(img_dilation.copy(),
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

        for i, ctr in enumerate(sorted_ctrs):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(ctr)

            # show ROI
            if (h > 40):
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, i*10, 0), 2)
                boxCount = 1 + boxCount
        cv2.imshow("roi", image)
        cv2.waitKey(25)

        return boxCount

    def dontKillThePedestrian(self):
        t = self.h/3
        b = 2*self.h/3
        l = self.w/4
        r = 3*self.w/4
        change = self.frame[t:b, l:r] - self.last[t:b, l:r]
        change = cv2.medianBlur(change, 9)
        gray = cv2.cvtColor(change, cv2.COLOR_BGR2GRAY)
        bw = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)[1]
        bw = cv2.medianBlur(bw, 5)
        boxCount = self.roi(bw)

        if (boxCount != 0 or np.sum(bw) > 20000000):
            self.stop()
        else:
            self.notKillin = False
        self.lastCross = rospy.get_rostime().secs

    def atCrosswalk(self):
        red = self.red_filter()

        for i in range(8, 10):
            s = red[i*self.h/10, self.w/4:3*self.w/4]
            # check how red the slice is
            if np.sum(s) > 10000:
                cv2.circle(self.frame, (self.w/2, i*self.h/10), 20, (255, 0, 0), -1)
                return True
        return False

    def follow(self, state, curb="R"):
        if curb == "R":
            if state <= 21*self.slice_num/30:
                self.move("L")
            elif state >= 24*self.slice_num/30:
                self.move("R")
            else:
                self.move("F")
        else:
            if state <= 2*self.slice_num/30:
                self.move("L")
            elif state >= 6*self.slice_num/30:
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
