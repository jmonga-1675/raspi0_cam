#!/usr/bin/env python2.7
# Credit: Adrian Rosebrock
# https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
 
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy

print("Starting...")

# init node
rospy.init_node("camera_node")
pub = rospy.Publisher("kamigami/img_raw", Image, queue_size=1)
 
# Initialize the camera
camera = PiCamera()
bridge = CvBridge()
 
# Set the camera resolution
# camera.resolution = (640, 480)
# camera.resolution = (320, 240)
# camera.resolution = (160, 128)
camera.resolution = (64, 64)
 
# Set the number of frames per second
camera.framerate = 60
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=camera.resolution)
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
 
# Capture frames continuously from the camera
counter = 0
start = time.time()
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    if rospy.is_shutdown():
        break
    # counter += 1
    # Grab the raw NumPy array representing the image
    # image = frame.array[240:400, 180:300]
    image = frame.array
    image_msg = bridge.cv2_to_imgmsg(image, encoding="rgb8")
    pub.publish(image_msg)
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
end = time.time()
print("FPS: %f" % (counter/(end - start)))
