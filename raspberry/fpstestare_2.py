from imutils.video import VideoStream 
import cv2
import numpy as np
import time

# Background subtraction algortihm
backSub = cv2.createBackgroundSubtractorKNN()

# Using Pi Camera
PiCamera = True
# Set initial frame size.
frameSize = (1280, 720)

# Start camera
video = VideoStream(src=0, usePiCamera=PiCamera, resolution=frameSize,framerate=32).start()

time.sleep(2)


num_frames = 1;

# Grab a few frames
while True:

    # Start time
    start = time.time()

    frame = video.read()


    fgMask = backSub.apply(frame)

    sum = 0
    N = 1
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
    print(fps)
    cv2.putText(fgMask, "FPS: " + str(round(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255))

    cv2.imshow('fgMask', frame)



    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break



cv2.destroyAllWindows()
