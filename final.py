import cv2
import numpy as np
import sys
import thread

from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
Motor1A = 5
Motor1B = 7
Motor1E = 3
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
camera = PiCamera()

# allow the camera to warmup
time.sleep(0.1)
cap = cv2.VideoCapture(1)
k=0;
l=0;

def motor():
    while 1:
        GPIO.output(Motor1E,GPIO.HIGH)
        sleep(0.01)
        GPIO.output(Motor1E,GPIO.LOW) 
        
try :
    thread.start_new_thread( motor, () )
except:
    pass


while 1:
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")    
    frame1 = rawCapture.array
    _, frame1 = cap.read()
    j=0;
    frame = frame1[20:250, 10:700] # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    #cv2.imshow("cropped", crop_img)
    #cv2.imshow('frame',frame)

    for i in range(0,1000):
     j=j+1;   
    gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower_red = np.array([170,120,50])
    upper_red = np.array([180,255,255])
    
    lower_green = np.array([50,50,100])
    upper_green = np.array([80,255,255])
    

    # Threshold the HSV image to get only red and green colors
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = cv2.inRange(hsv, lower_green, upper_green)
    mask=mask1+mask2

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)      

    zg = (mask1 >250).sum()
    zr = (mask2 >250).sum()
    za=zg-zr+100
    if za<0:
     cirles=cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 10)# ret=[[Xpos,Ypos,Radius],...]
     if cirles!=None:
         k=k+1
         l=0
         if k>2:
          print "Red Light"
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.LOW)
          
          while 1:
           rawCapture = PiRGBArray(camera)
           camera.capture(rawCapture, format="bgr")    
           frame1 = rawCapture.array
           _, frame1 = cap.read()
           frame = frame1[20:250, 10:700]
           for i in range(0,1000):
              j=j+1;   
           gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),5)
           hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
           lower_red = np.array([170,120,50])
           upper_red = np.array([180,255,255])
    
           lower_green = np.array([50,50,100])
           upper_green = np.array([80,255,255])
           mask2 = cv2.inRange(hsv, lower_red, upper_red)
           mask1 = cv2.inRange(hsv, lower_green, upper_green)
           mask=mask1+mask2
           res = cv2.bitwise_and(frame,frame, mask= mask)
           zg = (mask1 >250).sum()
           zr = (mask2 >250).sum()
           za=zg-zr
           if za>0:
               cirles=cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 10)
               if cirles!=None:
                 print "mov"
                    GPIO.output(Motor1A,GPIO.HIGH)
                    
         
                 break
   
          #print cirles
     else :
         k=0
         l=l+1
         if l>10:
          print "move"
          GPIO.output(Motor1A,GPIO.HIGH)
          
     #cv2.imshow('video',gray)
    else:
        k=0
        l=0;
        print("move!!!!!")
        GPIO.output(Motor1A,GPIO.HIGH)
    if cv2.waitKey(1)==27:# esc Key
        break
cap.release()
cv2.destroyAllWindows()


 
            
 
        
