#!/usr/bin/env python2.7
# Credit: Adrian Rosebrock
# https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
 
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library

print("Starting...")

# Initialize the camera
camera = PiCamera()
 
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
counter_lim = 200
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    counter += 1
    if counter == counter_lim:
        break
    # Grab the raw NumPy array representing the image
    # image = frame.array[240:400, 180:300]
    # image = frame.array
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
end = time.time()
print("FPS: %f" % (counter_lim/(end - start)))
