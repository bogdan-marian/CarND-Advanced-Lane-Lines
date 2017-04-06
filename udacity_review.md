# worthy of noting sections from the review

## Pipeline (test images)

**A method or combination of methods (i.e., color transforms, gradients) has been used to create a binary image 
containing likely lane pixels. There is no "ground truth" here, just visual verification that the pixels identified 
as part of the lane lines are, in fact, part of the lines. Example binary images should be included in the writeup 
(or saved to a folder) and submitted with the project.**

Good job extracting the lane lines! An idea for more robust extraction is to try color thresholding in all the 
RGB, HSV and HSL channels for your yellows and whites! By using color thresholding you are able to make the lane 
detection more robust by relying less on gradients for good results! Furthermore, thresholding is a lot faster in 
terms of processing than gradients!

Here is some sample code to play around with, it should help with more tricky areas!

```
HSV = cv2.cvtColor(your_image, cv2.COLOR_RGB2HSV)

# For yellow
yellow = cv2.inRange(HSV, (20, 100, 100), (50, 255, 255))

# For white
sensitivity_1 = 68
white = cv2.inRange(HSV, (0,0,255-sensitivity_1), (255,20,255))

sensitivity_2 = 60
HSL = cv2.cvtColor(your_image, cv2.COLOR_RGB2HLS)
white_2 = cv2.inRange(HSL, (0,255-sensitivity_2,0), (255,255,sensitivity_2))
white_3 = cv2.inRange(your_image, (200,200,200), (255,255,255))

bit_layer = your_bit_layer | yellow | white | white_2 | white_3
```

## Pipeline (video)

**The image processing pipeline that was established to find the lane lines in images successfully processes the video. 
The output here should be a new video where the lanes are identified in every frame, and outputs are generated regarding 
the radius of curvature of the lane and vehicle position within the lane. The pipeline should correctly map out curved 
lines and not fail when shadows or pavement color changes are present. The output video should be linked to in the writeup 
and/or saved and submitted with the project.**

Your video looks great! In addition to other filtering mechanisms like averaging the polynomial coefficients and rejecting
outliers. You can use cv2.matchShapes as a means to make sure the final warp polygon is of quality before using. 
OpenCV's matchShapes, compares two shapes and returns a similarly index, with 0 being identical shapes. 
You can use this to make sure the polygon for your next frame is close to what it is expected to look like and if not
you can elect to use old polygon instead. This way you can let your algorithm be really good when it can and when it 
can just fake it until a few frames later when it produces good results.

Here is an example:

```
# Early in the code before pipeline
global polygon_points_old
polygon_points_old = None


# In the pipeline

if (polygon_points_old == None):
    polygon_points_old = polygon_points

a = polygon_points_old
b = polygon_points
ret = cv2.matchShapes(a,b,1,0.0)

if (ret < 0.045):
    # Use the new polygon points to write the next frame due to similarities of last successfully written polygon area

    polygon_points_old = polygon_points

else:
    # Use the old polygon points to write the next frame due to irregularities
    # Then write the out the old polygon points
    # This will help only use your good detections
```
