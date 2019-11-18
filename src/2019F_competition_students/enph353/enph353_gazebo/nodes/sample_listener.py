import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


bridge = CvBridge()


def callback(data):
    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    cv2.imshow("img", img)
    cv2.waitKey(25)


if __name__ == '__main__':
    rospy.init_node('image_converter', anonymous=True)
    listener = rospy.Subscriber("car_pics", Image, callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
