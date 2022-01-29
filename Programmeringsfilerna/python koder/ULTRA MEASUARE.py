import RPi.GPIO as GPIO
import time
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 12
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
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
import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
    ser.reset_input_buffer()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    print("Distance is ",distance())
    time.sleep(0.5)
    
 
 
        # Reset by pressing CTRL + C
    if KeyboardInterrupt == True :
        print("Measurement stopped by User")
        GPIO.cleanup()
        break
