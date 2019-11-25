import cv2
import numpy as np

img = cv2.imread("/home/pham/enph353_ws/src/2019F_competition_students/enph353/enph353_gazebo/media/snaps/144b.JPEG", cv2.COLOR_RGB2HSV)

lower_red = np.array([80,55,0])
upper_red = np.array([120,205,255])

mask = cv2.inRange(img, lower_red, upper_red)

cv2.imshow("img", mask)
cv2.imshow("img2", img)
cv2.waitKey(0)
