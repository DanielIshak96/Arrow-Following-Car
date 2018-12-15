# Arrow-Following-Car
A differential robot that uses a camera to follow arrows.

## Table of contents
- [Team Members](#team-members)
- [Project Demo](#project-demo)
- [Description](#description)
- [Usage](#usage)
- [Platforms required](#Platforms required)
- [Project Video](#project-video)


## Team Members
- Ahmed Abdelmoneim
- Abanoub Adel
- Ahmed Waleed
- Ahmed Sayed
- Daniel Ashraf
- Donia Abdelhamid


## Project Demo
This project was designed to detect the direction of arrows and follow them using opencv library.The arrows controlled Robot is based on RasperryPi, WebCam and L293D Motor Driver. 

The low-level control architecture was simple depending on the GPIOs of our controller “Raspberry pi” where we used a motor driver to drive the wheels motors.
So the high-level control algorithm which takes the image and processes it resulting in determining the arrow direction make use of the low-level functions to drive the car.

## Description
Here is a glance at the flow of the code:
First, the right side motor and the left side motor are connected to the L298 Dual H-Bridge Motor Driver,
which is going to receive the signal from the raspberry pi to provide the required movement. Pin 17 and pin 27 are connected to the driver.

Second, the images of the arrows are inserted using the "imread" function, then the features of the images are extracted using the SIFT (scale invariant feature transform) function.

Third, the GPIO (general purpose input output) pins which are connected to the driver are initialized.

Forth, the sift function is enabled and the parameters of the flann matcher are set.

Fifth, The image from the camera is compared to the dataset images and see if it matches any of them in order to detect in which direction it will move.
 
Finally, according to the matching an output signal will be sent to the motors to provide the required movement. In case of forward the two motors will work together,
 to move to the left the right motor will work and to move to the right the left motor will work to move in the required direction. 


### Usage
 General tips on how to use/add/remove features.

This code was build and tested using a Raspberry Pi 3 with Opencv3.3 and Python3 installed and a Logitech camera. 
The code originally runs on 3 different test images, 2 driven motors (located on pins 17,27) and 256x256 5fps video.

To edit the size of the video you should alter the following commands
	cam.set(cv2.CAP_PROP_FRAME_WIDTH,256)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT,256)
  

To increase/decrease the FPS
	cam.set(cv2.CAP_PROP_FPS,5)

More training images can be added through
	img_N = cv2.imread("Your_image.jpg")

For each image added, add their corresponding feature vector & matches
	kp_N, desc_N = sift.detectAndCompute(img_N, None)
	matches_N = flann.knnMatch(desc_1, desc_N, k=2)


New pins should be defined according to BCM (as defined in the code) for any additional features that will be added.

A problem was found while testing realtime while using the time.sleep() function where the camera kept old/unwanted frames and thus the code behaved upnormal,
this was overcome by releasing the camera then re-opening it once again.





### Platforms required

The main platforms and libraries needed are:
 - OpenCV
 - RPi.GPIO
 

## Project Video
[Youtube](https://www.youtube.com/watch?v=Mj8o48O8rrs&feature=youtu.be)

