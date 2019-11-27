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
    current_spot = getSpotChars(img)
    img1 = img
    chars = getPlateChars(img1)
    cv2.imshow('frefre',img)
    cv2.waitKey(25) 
    spotReadings[frameCount % pics_per_car, 0] = current_spot
    # Add character guesses to plateReadings array
    for i in range(4):
        plateReadings[frameCount % pics_per_car, i] = chars[i]
        

    # After 5 frames, get modal guess for each character
    if (frameCount % pics_per_car == 0):
        goodRows = []
        goodSpots = []
        for i in range(pics_per_car-1, -1, -1):
            if not (plateReadings[i] == ['0', '0', '0', '0']).all():
                goodRows.append(i)
        for i in range(len(spotReadings)):
            if not (spotReadings[i] == 'x' ):
                if (spotReadings[i] == 'z' ):
                    print('Spot changed')
                    print(spot)
                    spotReadings[i] = str(int(spot)+1)
                goodSpots.append(i)


        try:
            bestGuess = ''.join(mode(plateReadings[goodRows, :])[0][0])
            bestSpotGuess = ''.join(mode(spotReadings[goodSpots, :])[0][0])
            print(plateReadings)
            print(plateReadings[goodRows, :])
            print(bestGuess)
            print(spotReadings[goodSpots, :])
            print(bestSpotGuess)
            if (bestSpotGuess == '0'):
                bestSpotGuess == '1'
            spot = bestSpotGuess
            submitPlate(bestGuess)
        except IndexError:
            print("Could not read plate")


def submitPlate(plate):
    global spot
    plate_pub.publish("123,456," + str(spot) + "," + plate.upper())
  

if __name__ == '__main__':
    rospy.init_node('image_processor', anonymous=True)
    listener = rospy.Subscriber("car_pics", Image, callback)
    plate_pub = rospy.Publisher('/license_plate', String, queue_size=1)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
