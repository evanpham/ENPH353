import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
from license_reader import getPlateChars
from spot_finder import getSpotChars
import numpy as np
from scipy.stats import mode

bridge = CvBridge()
frameCount = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2
textLocation = (10, 200)
initialized = False
pics_per_car = 5
plateReadings = np.empty((pics_per_car, 4), dtype=str)
spotReadings = np.empty((pics_per_car, 1), dtype=str)
spot = 2


def callback(data):
    global frameCount, plateReadings, spot
    # Increment frameCount
    # Every this node gets 5 frames per car passed
    frameCount = frameCount + 1

    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    img1 = img
    chars = getPlateChars(img1)
    # cv2.imshow('frefre',img)
    # cv2.waitKey(25) 
    # Add character guesses to plateReadings array
    for i in range(4):
        plateReadings[frameCount % pics_per_car, i] = chars[i] 

    # After 5 frames, get modal guess for each character
    if (frameCount % pics_per_car == 0):
        goodRows = []
        for i in range(pics_per_car-1, -1, -1):
            if not (plateReadings[i] == ['0', '0', '0', '0']).all():
                goodRows.append(i)

        try:
            bestGuess = ''.join(mode(plateReadings[goodRows, :])[0][0])
            print(plateReadings)
            print(plateReadings[goodRows, :])
            print(bestGuess)
            submitPlate(bestGuess)
        except:
            print("Could not read plate")
            spot = spot + 1


def submitPlate(plate):
    global spot
    if spot != 7:
        plate_pub.publish("123,456," + str(spot) + "," + plate.upper())
    elif spot == 8:
        plate_pub.publish("123,456,7," + plate.upper())
    elif spot == 9:
        plate_pub.publish("123,456,8," + plate.upper())
    else:
        plate_pub.publish("123,456,1," + plate.upper())

    spot = spot + 1


if __name__ == '__main__':
    rospy.init_node('image_processor', anonymous=True)
    listener = rospy.Subscriber("car_pics", Image, callback)
    plate_pub = rospy.Publisher('/license_plate', String, queue_size=1)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
