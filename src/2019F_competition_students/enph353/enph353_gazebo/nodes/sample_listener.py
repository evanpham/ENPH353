import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from license_reader import getPlateChars
import numpy as np
from scipy.stats import mode


bridge = CvBridge()
frameCount = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2
initialized = False
plateReadings = np.zeros((5, 4))


def callback(data):
    global frameCount, initialized, plateReadings
    frameCount = frameCount + 1
    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    w, h = img.shape[0:2]
    chars = getPlateChars(img, initialized)
    for i in range(4):
        plateReadings[frameCount % 5, i] = chars[i]

    # # Gets plate characters from image
    if (frameCount % 5 == 0):
        for i in range(4, -1, -1):
            print(i)
            print(plateReadings[i])
            if (plateReadings[i] == [0, 0, 0, 0]).all():
                print("del")
                plateReadings = np.delete(plateReadings, i, axis=0)
        try:
            bestGuess = [mode(plateReadings[0, :])[0][0],
                         mode(plateReadings[1, :])[0][0],
                         mode(plateReadings[2, :])[0][0],
                         mode(plateReadings[3, :])[0][0]]
            plate = ''.join(str(bestGuess))
            bottomLeft = (10, w/2)
            cv2.putText(img, plate, bottomLeft, font, fontScale, fontColor, lineType)
            cv2.imshow("img", img)
            cv2.waitKey(25)
            print(plateReadings)
            print(bestGuess)
        except IndexError:
            print("Could not read plate")

        plateReadings = np.zeros((5, 4))

    if not initialized:
        initialized = True

if __name__ == '__main__':
    rospy.init_node('image_converter', anonymous=True)
    listener = rospy.Subscriber("car_pics", Image, callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
