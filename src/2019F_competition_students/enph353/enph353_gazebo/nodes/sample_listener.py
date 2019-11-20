import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from license_reader import getPlateChars
import numpy as np
from scipy.stats import mode
from keras.models import load_model

bridge = CvBridge()
frameCount = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2
textLocation = (10, 200)
initialized = False
plateReadings = np.empty((5, 4), dtype=str)


def callback(data):
    global frameCount, plateReadings

    frameCount = frameCount + 1
    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    chars = getPlateChars(img)

    for i in range(4):
        plateReadings[frameCount % 5, i] = chars[i]

    # Gets plate characters from image
    if (frameCount % 5 == 0):
        for i in range(4, -1, -1):
            if (plateReadings[i] == ['0', '0', '0', '0']).all():
                plateReadings = np.delete(plateReadings, i, axis=0)
        try:
            bestGuess = str(mode(plateReadings)[0][0])
            plate = ''.join(str(bestGuess))
            print(plateReadings)
            print(bestGuess)
            # cv2.putText(img, bestGuess, textLocation, font, fontScale, fontColor, lineType)
            # cv2.imshow("img", img)
            # cv2.waitKey(25)
        except IndexError:
            print("Could not read plate")
        plateReadings = np.empty((5, 4), dtype=str)


if __name__ == '__main__':
    rospy.init_node('image_converter', anonymous=True)
    listener = rospy.Subscriber("car_pics", Image, callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
