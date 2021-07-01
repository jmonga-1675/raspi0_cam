#!/usr/bin/env python2.7
# Credit: Adrian Rosebrock
# https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
 
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
# import cv2 # OpenCV library
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy

# init node
rospy.init_node("camera_node")
pub = rospy.Publisher("kamigami/img_raw", Image, queue_size=10)
 
# Initialize the camera
camera = PiCamera()
bridge = CvBridge()
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
 
# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    if rospy.is_shutdown():
        break
     
    # Grab the raw NumPy array representing the image
    image = frame.array[240:400, 180:300]
    image_msg = bridge.cv2_to_imgmsg(image, encoding="rgb8")
    pub.publish(image_msg)
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
