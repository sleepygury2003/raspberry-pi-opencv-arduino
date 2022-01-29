import numpy
import cv2
from imutils.video import VideoStream  
import time

# Background subtraction algortihm
backSub = cv2.createBackgroundSubtractorKNN()

# Haarcascade classifier modle for detect face
face_cascade = cv2.CascadeClassifier('stop.xml')

# Using Pi Camera
PiCamera = True


# Set initial frame size.
frameSize = (500, 300)

# Setup video stream
vs = VideoStream(src=0, usePiCamera=PiCamera, resolution=frameSize,framerate=32).start()

# Allow camera to setup.
time.sleep(2.0)
i = 0

stop = False
import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
    ser.reset_input_buffer()
fps = vs.get(cv2.CAP_PROP_FPS)

# Number of frames to capture
num_frames = 1;


while 1:
     # Start time
    start = time.time()

    # Read Video steram
    ret, frame = vs.read()
    if frame is None:
        print("No frame")
        break

    fgMask = backSub.apply(frame)

    sum = 0
    N = 300
    for i in range(0, N):
        for j in range(0, N):
            sum += 1

    kernel = np.ones((5,5), np.uint8)

    fgMask = cv2.erode(fgMask, kernel, iterations=1)
    fgMask = cv2.dilate(fgMask, kernel, iterations=1)


    # End time for whole program running 120 frames
    end = time.time()

    # Time elapsed
    seconds = end - start
    #print ("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds
    #print("Estimated frames per second : {0}".format(fps))

    cv2.putText(fgMask, "FPS: " + str(round(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255))

    cv2.imshow('fgMask', fgMask)



    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break



# Release camera
video.release()
