import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from license_reader import getPlateChars


bridge = CvBridge()
frameCount = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2


def callback(data):
    global frameCount
    frameCount = frameCount + 1
    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    w, h = img.shape[0:2]
    # # Gets plate characters from image
    chars = getPlateChars(img)
    if (frameCount % 5 == 0):
        plate = ''.join(chars)
        bottomLeft = (10, w/2)
        cv2.putText(img, plate, bottomLeft, font, fontScale, fontColor, lineType)
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
