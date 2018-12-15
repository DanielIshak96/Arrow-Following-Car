#importing numpy,cv2.etc

import numpy as np 
import cv2
import RPi.GPIO as GPIO
import time

#here we open the camera, defining the FPS and resolution which are tuned to make the algorithm work in the real time  
def CameraOpen():
    cam.open(0)
    cam.set(cv2.CAP_PROP_FPS,5)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,256)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,256)
    


# set mode for GPIO to BCM which is a nomenclature for pins definition 
GPIO.setmode(GPIO.BCM)

# start capturing images from camera 
cam = cv2.VideoCapture(0)

# setting the image used for training to img2,img3& img4
img2 = cv2.imread("Forward2.jpg") #train
img3 = cv2.imread("Left2.jpg") #train
img4 = cv2.imread("Right2.jpg") #train

# enable sift algorithm in order to extract features from the training images 
sift = cv2.xfeatures2d.SIFT_create()
kp_2, desc_2 = sift.detectAndCompute(img2, None) # forward
kp_3, desc_3 = sift.detectAndCompute(img3, None) # Left
kp_4, desc_4 = sift.detectAndCompute(img4, None) # Right

#setting the pins
RM = 27
LM = 17 
#some pin number (not anything dedicated, just a generic)
 #some pin number (not anything dedicated, just a generic)
GPIO.setup(LM,GPIO.OUT) #====>the pin fires at full blast here
GPIO.setup(RM,GPIO.OUT)#====>the pin fires at full blast here
GPIO.cleanup() #=====> this is the only way I can get the pin to stop

#this threshold is set after tuning in order define the zone in which the camera doesn’t see any of the training images (it considered as the number of the minimum good points)
Threshold=14
while 1:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RM,GPIO.OUT)
    GPIO.setup(LM,GPIO.OUT) #====>the pin fires at full blast here


#putting the camera image in img
    ret, img = cam.read()
    if ret:
        k = cv2.waitKey(10) 
    if k == 27: #press Esc to exit
       break
# 1) Check if 2 images are equals
    
        
    # enable sift algorithm in order to extract features from the camera image
    kp_1, desc_1 = sift.detectAndCompute(img, None)
    
    # setting the parameter of the flann matcher 
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


    # detect & show good points between camera image and Fwd image 
    for m, n in matches1:
        if m.distance < ratio*n.distance:
            GoodFwd.append(m)
    print("1=",len(GoodFwd))
    result1 = cv2.drawMatches(img, kp_1, img2, kp_2, GoodFwd, None)

    cv2.imshow("result1", result1)
    #######

    # detect & show good points between camera image and Left image 
    for m, n in matches2:
        if m.distance < ratio*n.distance:
            GoodLeft.append(m)
    print("2=",len(GoodLeft))
    result2 = cv2.drawMatches(img, kp_1, img3, kp_3, GoodLeft, None)

    cv2.imshow("result2", result2)
    
    #####
    # detect & show good points between camera image and Right image 
    for m, n in matches3:
        if m.distance < ratio*n.distance:
            GoodRight.append(m)
    print("3=",len(GoodRight))
    result3 = cv2.drawMatches(img, kp_1, img4, kp_4, GoodRight, None)

    cv2.imshow("result3", result3)
    

# the following if conditions implement the following algorithm, the image which have the maximum number of good points matched with the camera image and the number of the good points is greater than the threshold is the image which the camera looks at it  

    if (len(GoodFwd)>len(GoodLeft)) and (len(GoodFwd)>len(GoodRight) and len(GoodFwd)>Threshold):
       print("forward")
	
	# enable the 4 wheels 
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
	
# release the camera while delay it’s a very important 
       cam.release()
       time.sleep(1) #=====>this is respected and followed
# reopening the camera
       CameraOpen()
       
       
    if len(GoodLeft)>len(GoodFwd) and len(GoodLeft)>len(GoodRight) and len(GoodLeft)>Threshold:
       print("left")
	
# enable the right wheels 
       GPIO.output(LM,False) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's

# release the camera while delay it’s a very important 
       cam.release()
       time.sleep(0.65) #=====>this is respected and followed

    	# enable the 4 wheels 
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
       
       time.sleep(0.3) #=====>this is respected and followed

# reopening the camera
       CameraOpen()
       
    if len(GoodRight)>len(GoodLeft) and len(GoodRight)>len(GoodFwd) and len(GoodRight)>Threshold:
       print("right")
      
       
# enable the left wheels 
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,False) #=====>this is ignored by all 4 Pi's

# release the camera while delay it’s a very important 
       cam.release()
       time.sleep(0.65) #=====>this is respected and followed

    	# enable the 4 wheels 
       GPIO.output(LM,True) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,True) #=====>this is ignored by all 4 Pi's
       
       time.sleep(0.3) #=====>this is respected and followed

# reopening the camera
       CameraOpen()
       
# if the camera image don’t contain any of the training image then the RC car has to stop 
    if len(GoodFwd)<(Threshold+1) and len(GoodLeft)<(Threshold+1) and len(GoodRight)<(Threshold+1):
                           
       GPIO.output(LM,False) #=====>this is ignored by all 4 Pi's
       GPIO.output(RM,False) #=====>this is ignored by all 4 Pi's

    
cv2.waitKey(0)
cv2.destroyAllWindows()
GPIO.cleanup() #=====> this is the only way I can get the pin to stop
cam.release()

