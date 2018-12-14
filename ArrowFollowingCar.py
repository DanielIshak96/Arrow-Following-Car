import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

def CameraOpen():
    cam.open(0)
    cam.set(cv2.CAP_PROP_FPS,5)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,256)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,256)
    



GPIO.setmode(GPIO.BCM)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS,5)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,256)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,256)
img2 = cv2.imread("Forward2.jpg") #train
img3 = cv2.imread("Left2.jpg") #train
img4 = cv2.imread("Right2.jpg") #train

sift = cv2.xfeatures2d.SIFT_create()
kp_2, desc_2 = sift.detectAndCompute(img2, None)
kp_3, desc_3 = sift.detectAndCompute(img3, None)
kp_4, desc_4 = sift.detectAndCompute(img4, None)

#setting the pins
RM = 27
LM = 17 #some pin number (not anything dedicated, just a generic)
 #some pin number (not anything dedicated, just a generic)
GPIO.setup(LM,GPIO.OUT) #====>the pin fires at full blast here
GPIO.setup(RM,GPIO.OUT)#====>the pin fires at full blast here
GPIO.cleanup() #=====> this is the only way I can get the pin to stop
Threshold=14
while 1:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RM,GPIO.OUT)
    GPIO.setup(LM,GPIO.OUT) #====>the pin fires at full blast here
 

    ret, img = cam.read()
    #cam.grab()
    #retval, img =cam.retrieve(0)
    
    if ret:
        k = cv2.waitKey(10) 
    if k == 27: #press Esc to exit
       break
# 1) Check if 2 images are equals
    
        
    
    kp_1, desc_1 = sift.detectAndCompute(img, None)
    

    index_params= dict(algorithm=0,trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches1 = flann.knnMatch(desc_1, desc_2, k=2)
    matches2 = flann.knnMatch(desc_1, desc_3, k=2)
    matches3 = flann.knnMatch(desc_1, desc_4, k=2)

    ratio = 0.4
    GoodFwd =[]
    GoodLeft =[]
    GoodRight =[]

    for m, n in matches1:
        if m.distance < ratio*n.distance:
            GoodFwd.append(m)
    print("1=",len(GoodFwd))
    result1 = cv2.drawMatches(img, kp_1, img2, kp_2, GoodFwd, None)

    cv2.imshow("result1", result1)
    #######
    for m, n in matches2:
        if m.distance < ratio*n.distance:
            GoodLeft.append(m)
    print("2=",len(GoodLeft))
    result2 = cv2.drawMatches(img, kp_1, img3, kp_3, GoodLeft, None)

    cv2.imshow("result2", result2)
    
    #####
    for m, n in matches3:
        if m.distance < ratio*n.distance:
            GoodRight.append(m)
    print("3=",len(GoodRight))
    result3 = cv2.drawMatches(img, kp_1, img4, kp_4, GoodRight, None)

    cv2.imshow("result3", result3)
    
    if (len(GoodFwd)>len(GoodLeft)) and (len(GoodFwd)>len(GoodRight) and len(GoodFwd)>Threshold):
       print("forward")
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
       time.sleep(1) #=====>this is respected and followed
       
       
    if len(GoodLeft)>len(GoodFwd) and len(GoodLeft)>len(GoodRight) and len(GoodLeft)>Threshold:
       print("left")
       GPIO.output(LM,False) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
       time.sleep(0.65) #=====>this is respected and followed
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
       print("mashy 3ala tool")
       time.sleep(0.3) #=====>this is respected and followed

       
    if len(GoodRight)>len(GoodLeft) and len(GoodRight)>len(GoodFwd) and len(GoodRight)>Threshold:
       print("right")
      
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,False) #=====>this is ignored by all 4 Pi's

       time.sleep(0.65) #=====>this is respected and followed
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
       time.sleep(0.3) #=====>this is respected and followed

       
    if len(GoodFwd)<(Threshold+1) and len(GoodLeft)<(Threshold+1) and len(GoodRight)<(Threshold+1):
                           
       GPIO.output(LM,False) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,False) #=====>this is ignored by all 4 Pi's

    
cv2.waitKey(0)
cv2.destroyAllWindows()
GPIO.cleanup() #=====> this is the only way I can get the pin to stop
cam.release()
