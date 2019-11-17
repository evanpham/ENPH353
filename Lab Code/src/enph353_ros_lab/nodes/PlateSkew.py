import string
from skimage.filters import threshold_local
import random
from random import randint
import cv2
import numpy as np
import os
import argparse
import imutils
from PIL import Image, ImageFont, ImageDraw
from matplotlib import pyplot as plt
from numpy import loadtxt
from keras.models import load_model

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the
    # new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    widthA = int(widthA)
    widthB = int(widthB)
    if (widthA > widthB):
        maxWidth = widthA
    else:
        maxWidth = widthB
#   print(maxWidth)
# compute the height of the new image, which will be the
# maximum distance between the top-right and bottom-right
# y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    heightA = int(heightA)
    heightB = int(heightB)
    if (heightA > heightB):
        maxHeight = heightA
    else:
        maxHeight = heightB
#   print(maxHeight)

# now that we have the dimensions of the new image, construct
# the set of destination points to obtain a "birds eye view",
# (i.e. top-down view) of the image, again specifying points
# in the top-left, top-right, bottom-right, and bottom-left
# order
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [
        0, maxHeight-1]], dtype="float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
#   return the warped image
    return warped


image = cv2.imread('license_plate_test1.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
ratio = image.shape[0] / 500.0

image = imutils.resize(image, height=200)
orig = image
frame = image

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# define range of blue color in HSV
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_white = np.array([95, 95, 95])
upper_white = np.array([180, 180, 180])

maskw = cv2.inRange(rgb, lower_white, upper_white)

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame, frame, mask=mask)
resw = cv2.bitwise_and(frame, frame, mask=maskw)

total = cv2.add(res, resw)

# cv2.imshow('frame', frame)
# # cv2.imshow('mask', mask)
# cv2.imshow('white', resw)
# cv2.imshow('res', resw)
# cv2.imshow('total', total)
# cv2.waitKey()

gray = cv2.cvtColor(resw, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(gray, 75, 200)


# cv2.imshow('edged',edged)
# cv2.waitKey()
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour


cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

max = 0
second_max = 0



# # loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if our approximated contour has four points, then we
    # # can assume that we have found our screen
    cv2.drawContours(total, [approx], -1, (255, 255, 255), 2)
    cv2.imshow('tttt',total)
    print(len(approx))
    cv2.waitKey()
    if len(approx) == 4:
        if  cv2.contourArea(c)> max:
            screenCnt = approx
            max = cv2.contourArea(c)
        elif cv2.contourArea(c)>second_max:
            bottom_plate = approx
            second_max = cv2.contourArea(c)
print(approx)
cv2.drawContours(total, [screenCnt], -1, (55, 255, 255), 2)
cv2.drawContours(total, [bottom_plate], -1, (255, 25, 2), 2)
cv2.imshow('heyyyyy', total)
cv2.waitKey()


print(approx)
top_pts = screenCnt.reshape(4, 2)
bottom_pts = bottom_plate.reshape(4, 2)

top = order_points(top_pts)
ttl = top[0]
ttr = top[1]
# (ttl, ttr, tbr, tbl) = top

bottom = order_points(bottom_pts)
# (btl, btr, bbr, bbl) = bottom 
bbr = bottom[2]
bbl = bottom[3]

bounding = screenCnt
bounding[0] = [[ttl[0],ttl[1]]]
bounding[1] = [[ttr[0],ttr[1]]]
bounding[2] = [[bbl[0],bbl[1]]]
bounding[3] = [[bbr[0],bbr[1]]]
print(bounding)
print(screenCnt)

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
# plt.clf()
cv2.drawContours(total, [screenCnt], -1, (255, 255, 255), 2)
cv2.imshow('resw', total)
cv2.waitKey()
# # apply the four point transform to obtain a top-down
# # view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2))

# # convert the warped image to grayscale, then threshold it
# # to give it that 'black and white' paper effect

# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# warped = (warped > T).astype("uint8") * 255

# # show the original and scanned images
print("STEP 3: Apply perspective transform")
# plt.clf()
cv2.imshow('warped', warped)
# cropped_plate = warped[35:50, 0:100]
# cv2.imshow('cropped', cropped_plate)
cv2.waitKey()

# # load model
# model = load_model('model.h5')
# # summarize model.
# model.summary()
# imgs = []
# imgs.append(warped)
# yp = np.array(imgs)
# print(cropped_plate.shape)
# print(yp.shape)
# predictions = model.predict(yp)

