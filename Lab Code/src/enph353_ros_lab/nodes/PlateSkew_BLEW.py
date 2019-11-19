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

def roi(image, orig):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    # cv2.imshow('gray', gray) 
    # cv2.waitKey(0) 

    #binary 
    ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY) 
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
    # orig = cv2.cvtColor(orig,cv2.COLOR_BGR2RGB)
    imgs = []

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        # Getting ROI
        roi = orig[y:y + h, x:x + w]
        
        # show ROI
        if (w*h>40 and w*h<300 and (w/h>.5 and w/h<2)):
            roi = cv2.resize(roi, (102,150))
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, i*10, 0), 2)
            imgs.append(roi)
            # cv2.rectangle(gray, (x, y), (x + w, y + h), (255, i*10, 0), 2)
            # cv2.imshow('segment no:'+str(i),roi)
            # cv2.waitKey()
    # cv2.imshow('segment no:'+str(i),gray)
    # cv2.waitKey()
    return imgs

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

def return_characters(chars,dict):
    labels = []
    if (len(chars) == 4):
        for index in range(0,2):
            letters = chars[index][10:35]
            labels.append(dict[str(np.argmax(letters)+10)])
        for index in range(2,4):
            numbers = chars[index][0:9]
            labels.append(dict[str(np.argmax(numbers))])
    else:
        labels = ['0','0','0','0']
    return labels





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

def return_Labels(image):
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

    height = image.shape[0]
    width = image.shape[1]
    half = 2*image.shape[0]/5

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
    lower_blue = np.array([110, 80, 50])
    upper_blue = np.array([130, 255, 255])



    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('frame', frame)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    # cv2.imshow('hsv', hsv)
    hued = cv2.cvtColor(res,cv2.COLOR_BGR2HSV)
    imgs = []
    imgs = roi(hued,orig)


    # load model
    model = load_model('model3.h5')
    # summarize model.
    # model.summary()
    yp = np.array(imgs)
    predictions = model.predict(yp)
    labels = return_characters(predictions,dict)

    return labels

