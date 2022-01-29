import cv2
from imutils.video import VideoStream  
import time
import RPi.GPIO as GPIO
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
    ser.reset_input_buffer()

# Haarcascade classifier model for detect stop sign
face_detector = cv2.CascadeClassifier('stop.xml')

# Using Pi Camera
PiCamera = True

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set initial frame size.
frameSize = (1280, 720)

# Setup video stream
vs = VideoStream(src=0, usePiCamera=PiCamera, resolution=frameSize,framerate=60).start()

# Allow camera to setup.
time.sleep(2.0)
i = 0

# distance from camera to object(face) measured
# centimeter
Known_distance =10

# width of face in the real world or Object Plane
# centimeter
Known_width = 3

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 12

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

stop = False

def signal():
    pass
    

def dista():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW

    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dista= (TimeElapsed * 34300) / 2


    return dista

# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame

    # return the distance
    return distance

def face_data(image):
    face_width = 0  # making face width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width


#reading reference_image from directory
ref_image = cv2.imread("ST.jpg")

# find the face width(pixels) in the reference_image
ref_image_face_width = face_data(ref_image)

# get the focal by calling "Focal_Length_Finder"
# stop sign width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)

while 1:
    # Read Video steram
    frame= vs.read()
    face_width_in_frame = face_data(frame)
    # Convert frame into grayscale
    
        # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
    Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)

        # draw line as background of text
    cv2.line(frame, (30, 30), (230, 30), RED, 32)
    cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
    if 25<Distance<50:
        pass
    elif Distance < 25:
        stop = True
    else:
        print("go")
    # Drawing Text on the screen
    cv2.putText(
            frame, f"Distance: {round(Distance, 2)} CM", (30, 35),
            fonts, 0.6, GREEN, 2)

    if stop == True:       
        c = "S"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
    else:
        c = "F"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))

    stop = False

    # Show result
    cv2.imshow('img',frame)
    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break
