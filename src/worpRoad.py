import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import camera

my_camera = camera.Camera()

def corners_unwarp(img):
    # Use my camera to remove distortion
    undist = my_camera.undistort(img)


    return warped

img = mpimg.imread('../output_images/worpTest.png')
worped_image = corners_unwarp(img)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()


ax1.imshow(img)
ax1.set_title('Original worped image', fontsize=40)

ax2.imshow(worped_image)
ax2.set_title('Transfored image', fontsize=40)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
plt.show()
