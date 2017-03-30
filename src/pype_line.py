import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import camera

#create a camera object
my_camera = camera.Camera()

#open first image and display it.
img = mpimg.imread('../camera_cal/calibration1.jpg')
plt.imshow(img)
plt.show()

#undistort the first image and show
test_undestorted = my_camera.undistort(img)
plt.imshow(test_undestorted)
plt.show()
