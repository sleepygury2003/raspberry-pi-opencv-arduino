import threading
import RPi.GPIO as GPIO
import cv2
from imutils.video import VideoStream  
import time


# Haarcascade classifier modle for detect face
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
vs = VideoStream(src=0, usePiCamera=PiCamera, resolution=frameSize,framerate=32).start()

# Allow camera to setup.
time.sleep(2.0)
i = 0

# distance from camera to object(Stop sign) measured
# centimeter
Known_distance =10

# width of Stop sign in the real world or Object Plane
# centimeter
Known_width = 3

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX
stop_sign = False
import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
    ser.reset_input_buffer()
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 12
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Global Variable
stop_sign = False
stop = False
go = False
ultra_stop = False
right = False
def dista():
    #Global Variable for ultra mersaure distance
    global dist
    global stop_sign
    if stop_sign == True:
        time.sleep(5)
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
     
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
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
    dist = (TimeElapsed * 34300) // 2
    
    if 3<dist<60:
        dist = True
     
    if dist > 60:
        dist = False
    if dist > 400:
        dist = None
      
def signal():# Send Data to Arduino
    #Global Variable for stop
    global stop
    global stop_sign
    global ultra_stop
    global right
    if stop_sign == True:
        time.sleep(5)
        #Deicde the measuere of ultra sensor if it is worth stop
    if dist == True:
        ultra_stop = True
    if dist == False:
        ultra_stop = False


    #Decide if the car stop or not
    if right == True:
        c = "R"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
        right = False
    if stop_sign == True:       
        if right == False:
            c = "S"
            print("Sending number " + str(c) + " to Arduino.")
            ser.write(str(c).encode('utf-8'))
            right = True
            stop = True
            
    if ultra_stop == True:
        if stop_sign == False:
            c = "S"
            print("Sending number " + str(c) + " to Arduino.")
            ser.write(str(c).encode('utf-8'))
            stop = True
    if stop_sign == False and ultra_stop == False and right == False:   
        stop = False
            
    if stop == False:
        c = "F"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
        

# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
def Distance_finder(Focal_Length, real_stop_width, stop_width_in_frame):
    distance = (real_stop_width * Focal_Length) / stop_width_in_frame

    # return the distance
    return distance

def stop_data(image):
    stop_width = 0  # making stop width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting stop in the image
    stop = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the stop detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in stop:
        # draw the rectangle on the stop
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting stop width in the pixels
        stop_width = w

    # return the stop width in pixel
    return stop_width


#reading reference_image from directory
ref_image = cv2.imread("ST.jpg")

# find the stop width(pixels) in the reference_image
ref_image_stop_width = stop_data(ref_image)

# get the focal by calling "Focal_Length_Finder"
# stop width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_stop_width)
while 1:
    #Create Thread
    t1 = threading.Thread(target=dista)
    t2 = threading.Thread(target=signal)
    if stop_sign == True:
        time.sleep(5)
        t1.start()
        t2.start()
    # starting thread 1 and 2
    if stop_sign == False:
        t1.start()
        t2.start()
    

    # Read Video steram
    frame= vs.read()
    stop_width_in_frame = stop_data(frame)
    # Convert frame into grayscale
    
        # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
    Distance = Distance_finder(
            Focal_length_found, Known_width, stop_width_in_frame)

        # draw line as background of text
    cv2.line(frame, (30, 30), (230, 30), RED, 32)
    cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
    if Distance<50:
        stop_sign == True
        stop = True      
    if Distance > 50:
        stop_sign == False
          
        
    # Drawing Text on the screen
    cv2.putText(
            frame, f"Distance: {round(Distance, 2)} CM", (30, 35),
            fonts, 0.6, GREEN, 2)
    #Deicde the measuere of ultra sensor if it is worth stop

    # Show result
    cv2.imshow('img',frame)
    k = cv2.waitKey(30) & 0xff
    
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
