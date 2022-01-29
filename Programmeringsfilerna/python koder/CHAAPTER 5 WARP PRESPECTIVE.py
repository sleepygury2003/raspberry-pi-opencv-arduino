# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np
 

 
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
imag = cv2.imread("/home/pi/card.jpg")
img = cv2.resize(imag,(500,500))

width,height = 250,350
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
pts2= np.float32([[0,0],[width,0],[0, height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)

imgOutput = cv2.warpPerspective(img, matrix,(width,height))

cv2.imshow("Image",img)
cv2.imshow("output", imgOutput)

cv2.waitKey(0)
