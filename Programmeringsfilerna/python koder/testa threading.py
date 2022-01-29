import RPi.GPIO as GPIO
import time
import threading
# https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
 
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import cv2 # OpenCV library
 
# Initialize the camera
camera = PiCamera()
camera.rotation = 180
 
# Set the camera resolution
camera.resolution = (300, 300)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(200, 200))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
 

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 12
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    time.sleep(0.5)
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
    distance = (TimeElapsed * 34300) / 2

    if 3<distance<100:       
        c = "R"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
        time.sleep(0.1)
 
    if distance>400:
        distance = False
    elif distance>100:       
        c = "F"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
        time.sleep(0.1)
  
    return distance
def kamera():
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
     
        # Grab the raw NumPy array representing the image
        image = frame.array
         
        # Display the frame using OpenCV
        cv2.imshow("Frame", image)
         
        # Wait for keyPress for 1 millisecond
        key = cv2.waitKey(1) & 0xFF
         
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
    ser.reset_input_buffer()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    t1 = threading.Thread(target=distance)
    t2 = threading.Thread(target=kamera)

    t1.start()
    t2.start()
  
    
 
 
        # Reset by pressing CTRL + C
    if KeyboardInterrupt == True :
        print("Measurement stopped by User")
        GPIO.cleanup()
        break
