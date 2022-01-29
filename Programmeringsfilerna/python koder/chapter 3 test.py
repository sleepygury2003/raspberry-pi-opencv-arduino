# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np
 

 
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
img = cv2.imread("/home/pi/test.jpg")
resized = cv2.resize(img, (500,400))
print(resized.shape)
imgcropped = img[0:200,200:500]

cv2.imshow("Image", resized)
cv2.imshow("Image rcropped",imgcropped)
cv2.waitKey(0)
