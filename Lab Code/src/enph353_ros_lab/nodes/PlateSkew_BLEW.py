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

def find_right_points(pts):
    
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect = np.zeros((2, 2), dtype="float32")
    print(pts)
    print(s)
    rect[0] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    # return the ordered coordinates
    return rect

def find_left_points(pts):
       
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect = np.zeros((2, 2), dtype="float32")
    rect[1] = pts[np.argmin(s)]
    print('left')
    print(pts)
    print(s)
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[0] = pts[np.argmax(diff)]
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

dict = {}
dict['0'] = '0'
dict['1'] = '1'
dict['2'] = '2'
dict['3'] = '3'
dict['4'] = '4'
dict['5'] = '5'
dict['6'] = '6'
dict['7'] = '7'
dict['8'] = '8'
dict['9'] = '9'
dict['10'] = 'a'
dict['11'] = 'b'
dict['12'] = 'c'
dict['13'] = 'd'
dict['14'] = 'e'
dict['15'] = 'f'
dict['16'] = 'g'
dict['17'] = 'h'
dict['18'] = 'i'
dict['19'] = 'j'
dict['20'] = 'k'
dict['21'] = 'l'
dict['22'] = 'm'
dict['23'] = 'n'
dict['24'] = 'o'
dict['25'] = 'p'
dict['26'] = 'q'
dict['27'] = 'r'
dict['28'] = 's'
dict['29'] = 't'
dict['30'] = 'u'
dict['31'] = 'v'
dict['32'] = 'w'
dict['33'] = 'x'
dict['34'] = 'y'
dict['35'] = 'z'

image = cv2.imread('test2.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
height = image.shape[0]
width = image.shape[1]
half = image.shape[0]/2

for h in range(height-half):
    for w in range(width):
        image[h,w] = [0,0,0]


# cv2.imshow('i',image)
# cv2.waitKey()
orig = image

# image = imutils.resize(image, height=200)
frame = image

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# define range of blue color in HSV
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])



# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame, frame, mask=mask)

cv2.imshow('frame', frame)
cv2.imshow('mask', mask)
cv2.imshow('res', res)
# cv2.imshow('hsv', hsv)
cv2.waitKey()

# gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(res, (3, 3), 0)
edged = cv2.Canny(gray, 55, 255)

# convert image to grayscale image
gray_image = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
 
# convert the grayscale image to binary image
ret,thresh = cv2.threshold(gray_image,15,255,0)
 
# calculate moments of binary image
M = cv2.moments(thresh)
 
# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
print(cX)

if cX>width/2.0:
    right = True
else:
    right = False
# cv2.imshow('edged',edged)
# cv2.imshow('gray', gray)
# cv2.waitKey()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]


if right:
    peri_left = cv2.arcLength(cnts[0], True)
    approx_left = cv2.approxPolyDP(cnts[0], 0.02 * peri_left, True)

    peri_right = cv2.arcLength(cnts[1], True)
    approx_right = cv2.approxPolyDP(cnts[1], 0.02 * peri_right, True)

    size_r = len(approx_right)
    size_l = len(approx_left)

    br, tr = find_left_points(approx_right.reshape(size_r,2))
    bl, tl = find_right_points(approx_left.reshape(size_l,2))
    # print('haiufhiuewhfiuehriu')
    # print(bl)
    # print(tl)
    # print(br)
    # print(tr)
    # cv2.waitKey()

else:
    peri_left = cv2.arcLength(cnts[1], True)
    approx_left = cv2.approxPolyDP(cnts[1], 0.02 * peri_left, True)

    peri_right = cv2.arcLength(cnts[0], True)
    approx_right = cv2.approxPolyDP(cnts[0], 0.02 * peri_right, True)

    size_r = len(approx_right)
    size_l = len(approx_left)

    br, tr = find_left_points(approx_right.reshape(size_r,2))
    bl, tl = find_right_points(approx_left.reshape(size_l,2))
    # print(bl)
    # print(tl)
    # print(br)
    # print(tr)
    # cv2.waitKey()


bounding = np.zeros((4,1, 2), dtype="float32")
bounding[0] = [tl[0],tl[1]]
bounding[1] = [tr[0],tr[1]]
bounding[3] = [bl[0],bl[1]]
bounding[2] = [br[0],br[1]]
# print(bounding)
# cv2.waitKey()

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
# plt.clf()
# cv2.drawContours(frame, bounding.astype(int), -1, (255, 255, 255), 0)
# cv2.imshow('resw', frame)
# cv2.waitKey()
# # apply the four point transform to obtain a top-down
# # view of the original image
warped = four_point_transform(orig, bounding.reshape(4, 2))

# # convert the warped image to grayscale, then threshold it
# # to give it that 'black and white' paper effect

# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# warped = (warped > T).astype("uint8") * 255

# # show the original and scanned images
print("STEP 3: Apply perspective transform")
# plt.clf()
# cv2.imshow('warped', warped)
# # cropped_plate = warped[35:50, 0:100]
# # cv2.imshow('cropped', cropped_plate)
# cv2.waitKey()

# gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# # dilation
# kernel = np.ones((10, 1), np.uint8)
# img_dilation = cv2.dilate(gray, kernel, iterations=1)
# cv2.imshow('blal',gray)
# cv2.waitKey()s
#grayscale 
hued = cv2.cvtColor(warped,cv2.COLOR_BGR2HSV)
# cv2.imshow('warpeeedd',hued)
gray = cv2.cvtColor(hued,cv2.COLOR_BGR2GRAY) 
# cv2.imshow('gray', gray) 
# cv2.waitKey(0) 

#binary 
ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY) 
# cv2.imshow('second', thresh) 
# cv2.waitKey(0) 

#dilation 
kernel = np.ones((1,1), np.uint8) 
img_dilation = cv2.dilate(thresh, kernel, iterations=1) 
# cv2.imshow('dilated', img_dilation) 
# cv2.waitKey(0)
# find contours
# cv2.findCountours() function changed from OpenCV3 to OpenCV4: now it have only two parameters instead of 3
cv2MajorVersion = cv2.__version__.split(".")[0]
# check for contours on thresh
if int(cv2MajorVersion) >= 4:
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# sort contours

sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
# print(len(sorted_ctrs))

imgs = []

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)

    # Getting ROI
    roi = warped[y:y + h, x:x + w]
    # show ROI
    if (w*h>40 and (w/h>.5 and w/h<2)):
        roi = cv2.resize(roi, (102,150))

        imgs.append(roi)
        # cv2.rectangle(gray, (x, y), (x + w, y + h), (255, i*10, 0), 2)
        # cv2.imshow('segment no:'+str(i),roi)
        # cv2.waitKey()



# cv2.imshow('hay',gray)  
# cv2.imshow('1',imgs[0])
# cv2.imshow('2',imgs[1])
# cv2.imshow('3',imgs[2])
# cv2.imshow('4', imgs[3])
# cv2.waitKey()
image = cv2.imread('0.png')
roi = cv2.resize(image, (102,150))
imgs.append(roi)
image = cv2.imread('3.png')
roi = cv2.resize(image, (102,150))
imgs.append(roi)
image = cv2.imread('b.png')
roi = cv2.resize(image, (102,150))
imgs.append(roi)
image = cv2.imread('y.png')
roi = cv2.resize(image, (102,150))
imgs.append(roi)
image = cv2.imread('c.png')
roi = cv2.resize(image, (102,150))
imgs.append(roi)
# load model
model = load_model('model.h5')
# summarize model.
# model.summary()
yp = np.array(imgs)
# print(yp.shape)
predictions = model.predict(yp)
# print(predictions.shape)
# print(len(predictions))
label = []
for index in range(len(predictions)):
    label.append(dict[str(np.argmax(predictions[index]))])
print(label)

