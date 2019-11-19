# This is now mostly a reference document for code which
# may be useful for the major ROS project
# Likely fineLine is useful, along with the code
# which saves video images to Frames directory

import cv2
from PlateSkew_BLEW import return_Labels


def findLine(image, height, width):
    crop_img = image[height-100:height, 0:width]
    # Grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Colour thresh
    ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Get center of mass
    M = cv2.moments(thresh)
    try:
        cX = int(M["m10"]/M["m00"])
        cY = int(M["m01"]/M["m00"])
    except:
        print("ahhhhhhhh")
        cX = 0
        cY = 0

    return (cX, cY)

image = cv2.imread('6.png')

print(return_Labels(image))
# # Set an image name for each frame and an frame number
# frameNum = 0
# imgName = "frame" + str(frameNum) + ".png"

# # Create VideoCapture object for frame iteration and find frame dimensions
# cap = cv2.VideoCapture('src/enph353_ros_lab/media/video/raw_video_feed.mp4')
# w = int(cap.get(3))  # Width in pixels, float
# h = int(cap.get(4))  # Height in pixels, float

# # Iterate on frames
# while cap.isOpened():
#     ret, frame = cap.read()

#     # If frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # Find coordinates of center of line
#     center = findLine(frame, h, w)
#     xPos = center[0]
#     yPos = center[1]

#     # Place white circle on center of line at bottom and show the frame
#     cv2.circle(frame, (int(xPos), int(h-20)), 10, (0, 200, 0), -1)
#     cv2.imshow('frame', frame)

#     # Can quit playback with q
#     if cv2.waitKey(1) == ord('q'):
#         break

#     # Save frame as image in /Frames and update img name for next frame
#     status = cv2.imwrite("Frames/" + imgName, frame)
#     imgName = imgName.replace(str(frameNum), str(frameNum + 1))
#     frameNum += 1

# # To see image matrix format
# print("frame")
# print(frame)

# # End video capture and playback
# cap.release()
# cv2.destroyAllWindows()
