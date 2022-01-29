# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np
# Initialize the camera
camera = PiCamera()
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray&#91;0])
    rowsAvailable = isinstance(imgArray&#91;0], list)
    width = imgArray&#91;0]&#91;0].shape&#91;1]
    height = imgArray&#91;0]&#91;0].shape&#91;0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray&#91;x]&#91;y].shape&#91;:2] == imgArray&#91;0]&#91;0].shape &#91;:2]:
                    imgArray&#91;x]&#91;y] = cv2.resize(imgArray&#91;x]&#91;y], (0, 0), None, scale, scale)
                else:
                    imgArray&#91;x]&#91;y] = cv2.resize(imgArray&#91;x]&#91;y], (imgArray&#91;0]&#91;0].shape&#91;1], imgArray&#91;0]&#91;0].shape&#91;0]), None, scale, scale)
                if len(imgArray&#91;x]&#91;y].shape) == 2: imgArray&#91;x]&#91;y]= cv2.cvtColor( imgArray&#91;x]&#91;y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = &#91;imageBlank]*rows
        hor_con = &#91;imageBlank]*rows
        for x in range(0, rows):
            hor&#91;x] = np.hstack(imgArray&#91;x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray&#91;x].shape&#91;:2] == imgArray&#91;0].shape&#91;:2]:
                imgArray&#91;x] = cv2.resize(imgArray&#91;x], (0, 0), None, scale, scale)
            else:
                imgArray&#91;x] = cv2.resize(imgArray&#91;x], (imgArray&#91;0].shape&#91;1], imgArray&#91;0].shape&#91;0]), None,scale, scale)
            if len(imgArray&#91;x].shape) == 2: imgArray&#91;x] = cv2.cvtColor(imgArray&#91;x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
img = cv2.imread("/home/pi/shape.png")

imggray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgblur= cv2.GaussianBlur(imggray,(7,7),1)

imgStack = stackImages(0.6([img, imggray,imgblur]))

cv2.imshow("image",imgStack)


cv2.waitKey(0)
