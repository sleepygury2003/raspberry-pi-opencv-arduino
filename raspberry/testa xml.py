
import cv2
from imutils.video import VideoStream  
import time

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

while 1:
    # Read Video steram
    img = vs.read()
    # Convert frame into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find faces in frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        # render a message on frame with no face detected
        cv2.putText(img, "NO STOP SIGN DETECTED", (340, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4,cv2.LINE_AA)
    else:
        # render a message on frame with face detected
        cv2.putText(img, "STOP SIGN DETECTED", (340, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4,cv2.LINE_AA)
        for (x,y,w,h) in faces:
            # Draw rectangle around every detected face
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imwrite(str(i)+'.png', img)
            i = i+1
            stop = True
    # Show result
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if stop == True:       
        c = "S"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
        time.sleep(0.1)
    else:
        c = "F"
        print("Sending number " + str(c) + " to Arduino.")
        ser.write(str(c).encode('utf-8'))
        time.sleep(0.1)
    stop = False
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
