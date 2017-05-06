#! /usr/bin/env python3

import cv2 # OpenCV
import sys

# Input image
image_path = sys.argv[1]

# Model parameters
dir_path = "/home/ptracton/anaconda3/share/OpenCV/haarcascades/" # Please modify this for your environment
filename = "haarcascade_frontalface_default.xml" # for frontal faces

model_path = dir_path + "/" + filename

# Create the classifier
clf = cv2.CascadeClassifier(model_path)

# Read the image
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces on image
faces = clf.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(60, 60),
    flags=cv2.CASCADE_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)
