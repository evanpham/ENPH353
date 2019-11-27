import string
from skimage.filters import threshold_local
import random
from random import randint
import cv2
import numpy as np
import os
import argparse
from PIL import Image, ImageFont, ImageDraw
from matplotlib import pyplot as plt
from numpy import loadtxt
from keras.models import load_model
import keras
from scipy.stats import mode


def roi(image, orig):
    border = 5
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    # cv2.imshow('gray', gray) 
    # cv2.waitKey(0) 

    #binary 
    ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY) 
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
        x = x-border
        y = y-border
        w = w+border*2
        h = h+border*2
        # show ROI
        if (w*h > 1000 and w*h < 4000):
            roi = thresh[y:y + h, x:x + w]
            roi = cv2.resize(roi, (20, 30))
            roi = np.expand_dims(roi,axis=2)
            imgs.append(roi)
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, i*10, 0), 2)


    # cv2.imshow('plateBBox', gray)
    # cv2.waitKey()
    return imgs


def return_characters(chars, dict):
    labels = []
    for index in range(len(chars)):
        letter = dict[str(np.argmax(chars[index]))]
        if(letter == 'p' and index < len(chars)-1):
            labels.append(letter)
            numbers = chars[index+1][0:10]
            labels.append(dict[str(np.argmax(numbers))])
            return labels
    labels = ['x','x']
    return labels

model = keras.initializers.Initializer()
loaded = False


def getSpotChars(image):
    global model, loaded
    if not loaded:
        model = load_model('modelbin_7.h5')
        loaded = True
    
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

    orig = image
    frame = image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    # cv2.imshow('gray', gray) 
    # cv2.waitKey(0) 

    #binary 
    ret, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY_INV) 
    # cv2.imshow('second', thresh) 
    # cv2.waitKey(0) 
    gray = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR) 
    # define range of blue color in HSV
    lower_blue = np.array([110, 80, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    hued = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    imgs = []
    imgs = roi(gray, orig)


    yp = np.array(imgs)
    if (len(yp)>0):
        predictions = model.predict(yp)
    # print(predictions)
        labels = return_characters(predictions, dict)
    # print(labels)
        return labels[1]
    else:
        return 'z'
