# -*- coding: utf-8 -*-

import math
import numpy as np
import re
import cv2
import string
import random

from collections import Counter
from matplotlib import pyplot as plt
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras import models
from keras import optimizers

from scipy import stats

from keras.utils import plot_model
from keras import backend

PATH = "../media/plates/pictures/"


def filename_parser(name):
	characters = list(name)
	labels = []
	labels.append(characters[6])
	labels.append(characters[7])
	labels.append(characters[8])
	labels.append(characters[9])
	return(labels)


def files_in_folder(folder_path):
	'''
	Returns a list of strings where each entry is a file in the folder_path.
	
	Parameters
	----------
	
	folder_path : str
		A string to folder for which the file listing is returned.
	'''
	files_A = !ls "{folder_path}"
	# The files when listed from Google Drive have a particular format. They are
	# grouped in sets of 4 and have spaces and tabs as delimiters.
	
	# Split the string listing sets of 4 files by tab and space and remove any 
	# empty splits.
	files_B = [list(filter(None, re.split('\t|\s', files))) for files in files_A]
	
	# Concatenate all splits into a single sorted list
	files_C = []
	for element in files_B:
		files_C = files_C + element
		
	files_C.sort()
	
	return files_C


def random_skew(image):
	# Find corner coordinates of image
	pts = np.array([
		[0, 0],
		[image.shape[1], 0],
		[image.shape[1], image.shape[0]],
		[0, image.shape[0]]], dtype = "float32")
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	# Get width of image
	width = tr[0] - tl[0]
	# Get height of image
	height = br[1] - tr[1]

	# Randomly move corners for skewing
	tl_skew = [tl[0]+random.randint(0,int(width/4)), tl[1]+random.randint(0,int(height/4))]
	tr_skew = [tr[0]-random.randint(0,int(width/4)), tr[1]+random.randint(0,int(height/4))]
	bl_skew = [bl[0]+random.randint(0,int(width/4)), bl[1]-random.randint(0,int(height/4))]
	br_skew = [br[0]-random.randint(0,int(width/4)), br[1]-random.randint(0,int(height/4))]

	# Create a random destination array for the corners of the image
	dst = np.array([tl_skew, tr_skew, br_skew, bl_skew], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	mode = tuple(map(int, stats.mode(image)[0][0][0]))
	print("most common pixels")
	print(np.unique(image.reshape(-1, image.shape[2]), axis=0, return_counts=True))
	warped = cv2.warpPerspective(image, M, (width, height), cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, borderValue=mode)

	# return the warped image
	return warped


def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect


def crop_plate_chars(img_path):
	# import image
	image = cv2.imread(img_path)
	# grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# binary
	ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
	# dilation
	kernel = np.ones((10, 1), np.uint8)
	img_dilation = cv2.dilate(thresh, kernel, iterations=1)

	# find contours
	# cv2.findCountours() function changed from OpenCV3 to OpenCV4: now it have only two parameters instead of 3
	cv2MajorVersion = cv2.__version__.split(".")[0]
	# check for contours on thresh
	if int(cv2MajorVersion) >= 4:
		print("V4+")
		ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	else:
		im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Sort contours and initialize cropped character image array
	sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
	cropped_chars = []

	for i, ctr in enumerate(sorted_ctrs):
		# Get bounding box
		x, y, w, h = cv2.boundingRect(ctr)

		# Filter to contours containing the plate characters
		if (120 < h and 140 > h):
			# Getting ROI and resizing to fit neural net inputs
			roi = cv2.resize(image[y:y + h, x:x + w], (102,150))
			cropped_chars.append(roi)

	return cropped_chars


# Display character images with predictions
def displayImage(img, prediction):
		plt.figure()
		plt.imshow(img)
		caption = ("label = " + str(prediction))
		plt.text(0.5, 0.5, caption, 
					 color='orange', fontsize = 20,
					 horizontalalignment='left', verticalalignment='top')


def split_image(path, img_file):
	'''
		Splits license plate images into four character images

		Path gives the directory path of the license plate images
		img_file is the name of the image file within the directory

		Returns a 2d array with column 1 containing the images as np arrays
		and column 2 containing the character shown in the corresponding image
	'''
	# Get array of plate character images
	cropped_chars = crop_plate_chars(path + img_file)

	# Use parser to find characters in plate from file name
	characters = filename_parser(img_file)
 
	# Put into answer key array
	ans_key = np.vstack(([cropped_chars[i], characters[i]] for i in range(len(characters))))
		
	return ans_key


def train_nn(datasize):
	'''
		Trains neural net to read license plate images

		Datasize determins the number of license plate images loaded 
		for training and testing

		Returns the trained model, the training data images, the 
		training data labels, the test data images, and the test
		data labels
	'''

	# Get file paths of license plate images
	files = files_in_folder(PATH)
	np.random.shuffle(files)

	# Not sure what to do with this
	CONFIDENCE_THRESHOLD = 0.01

	# Create training and test datasets from list of image files
	train_imgs, train_labels, test_imgs, test_labels = get_datasets(files[0:datasize])

	# Initialize keras neural net
	model = models.Sequential()
	model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(train_imgs[0].shape)))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(128, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(128, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Flatten())
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(512, activation='relu'))
	model.add(layers.Dense(36, activation='softmax'))
		
	# Compile neural net and fit to training data
	model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
	history = model.fit(train_imgs, train_labels, epochs=10)

	# Evaluate neural net on test data
	test_loss, test_acc = model.evaluate(test_imgs, test_labels, verbose=2)
	print('Test accuracy:' + str(test_acc))

	return (model, history, train_imgs, train_labels, test_imgs, test_labels)


def get_datasets(files):
	labels = ['0','1','2','3','4','5','6','7','8','9'] + list(string.ascii_uppercase)
	files_labeled = np.empty((0,2))
	for file in files:
		img = file
		print("loading " + img)
		files_labeled = np.vstack((files_labeled, split_image(PATH, img)))

	# Shuffles our dataset    
	np.random.shuffle(files_labeled)

	# Create x (images) and y (labels) sets 
	image_set = np.stack((random_skew(files_labeled[i,0]) for i in range(len(files_labeled))), axis=0)/255.               
	label_set = np.array([labels.index(label) for label in files_labeled[:,1]])

	# Split dataset into testing and training sets
	VALIDATION_SPLIT = 0.2
	cutoff = int(math.ceil(image_set.shape[0] * (1-VALIDATION_SPLIT)))
	print(cutoff)
	print("Total examples: {:d}\nTraining examples: {:f}\nTest examples: {:f}".
				format(image_set.shape[0],
				cutoff,
				image_set.shape[0]-cutoff))

	train_imgs = image_set[0:cutoff]
	train_labels = label_set[0:cutoff]
	test_imgs = image_set[cutoff:]
	test_labels = label_set[cutoff:]

	print(train_imgs.shape)
	print(test_imgs.shape)
	return (train_imgs, train_labels, test_imgs, test_labels)

(model, history, train_imgs, train_labels, test_imgs, test_labels) = train_nn(1)

for i in range(8):
	displayImage(train_imgs[i], train_labels[i])

model.summary()

"""MODAL COLOR IS SOMETIME NOT BG COLOR"""

predictions = model.predict(test_imgs)

for index in range(20):
	displayImage(test_imgs[index], test_labels[index])

correct = 0
for index in range(len(test_labels)):
	correct += 1 if (test_labels[index] == np.argmax(predictions[index])) else 0
print(float(correct)/len(test_labels))

path = "/content/drive/My Drive/ENPH353/enph353_cnn_lab/F.png"
skewed = np.array(Image.open(path))[:,:,0:3]
print(skewed.shape)
skewed = np.stack([skewed])
displayImage(skewed[0], np.argmax(model.predict([skewed])[0]))



