#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
import cv2


bridge = CvBridge()
last = time.time()
index = 0


def save(data):
    global last, index
    img = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("img", img)
    cv2.waitKey(25)

    if time.time() - last > .5:
        cv2.imwrite("../media/snaps/" + str(index) + "c.JPEG", img)
        print("saving frame " + str(index))
        index = index + 1
        last = time.time()


rospy.init_node("image_collector", anonymous=True)
sub = rospy.Subscriber("/R1/pi_camera/image_raw", Image, save)
rospy.spin()
