# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np
import tensoflow

 
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
img = np.zeros((512,512,3),np.uint8)
#print(img)
#img[200:300,100:300]=255,0,0

cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),3)
cv2.rectangle(img,(0,0),(250,350),(255,0,0),cv2.FILLED)
cv2.circle(img,(400,50),30,(255,255,0),5)

cv2.putText(img, " OPEN CV", (300,200),cv2.FONT_HERSHEY_COMPLEX,1,(0,150,0),1)

cv2.imshow("Image",img)

cv2.waitKey(0)
