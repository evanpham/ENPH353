# This is now mostly a reference document for code which
# may be useful for the major ROS project
# Likely fineLine is useful, along with the code
# which saves video images to Frames directory

import cv2
import numpy as np


def findLine(image, height, width):
    # Convert to binary image, and find all black pixels (the line)
    # Only looks at bottom 25 rows of pixels
    # Blurring and re-binarying helps remove false black pixels
    bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]
    bw = cv2.blur(bw, (10, 10))
    bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]

    pixels = []
    for x in range(width):
        for y in range(height-25, height):
            if (bw[y, x, :] == [0, 0, 0]).all():
                pixels.append([x, y])
    pixels = np.array(pixels)

    return pixels


# Set an image name for each frame and an frame number
frameNum = 0
imgName = "frame" + str(frameNum) + ".png"

# Create VideoCapture object for frame iteration and find frame dimensions
cap = cv2.VideoCapture('src/enph353_ros_lab/media/video/raw_video_feed.mp4')
w = int(cap.get(3))  # Width in pixels, float
h = int(cap.get(4))  # Height in pixels, float

# Iterate on frames
while cap.isOpened():
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Find coordinates of pixels on line
    pixels = findLine(frame, h, w)

    # Get all black pixels in the bottom 100 rows
    pixels = pixels[pixels[:, 1] > h-100]
    xPos = np.mean(pixels[:, 0])
    yPos = np.mean(pixels[:, 1])

    # Place white circle on center of line at bottom and show the frame
    cv2.circle(frame, (int(xPos), int(h-20)), 10, (0, 200, 0), -1)
    cv2.imshow('frame', frame)

    # Can quit playback with q
    if cv2.waitKey(1) == ord('q'):
        break

    # Save frame as image in /Frames and update img name for next frame
    status = cv2.imwrite("Frames/" + imgName, frame)
    imgName = imgName.replace(str(frameNum), str(frameNum + 1))
    frameNum += 1

# To see image matrix format
print("frame")
print(frame)

# End video capture and playback
cap.release()
cv2.destroyAllWindows()
