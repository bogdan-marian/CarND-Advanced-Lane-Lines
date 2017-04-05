## Writeup


**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/01_camera_calibration.png "Undistorted"
[image3]: ./output_images/03_pipe_line_result.png "Pipeline"
[image4]: ./output_images/04_warp.png "Warp"
[image6]: ./output_images/06_collored_lane.png "Colored"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

Because one of the classes in the jupiter notebook became really big I will
add reference tags to the python code that can be easily searched in the
notebook.  Examle: The main imports used by this project are refferenced by the `#ref_01_import_section` tag at the top of the Advanced-Lane-Lines.ipyn file
### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

This step is handled by the `__init__(self)` method of the Camera class refferenced by `# ref_02_camera_calibration` tag.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection. At the end i call `cv2.calibrateCamera()` and keep inside the class the returned values
```
self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, self.imageSize, None, None)
```
In order to facilitate distortion I have created the method `def undistort(self, img):` From now on I'm distorting images buy calling the camera undistort method.

I applied this distortion correction to the test image and obtained this result:

![alt text][image1]


### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
To demonstrate this step, I will describe how I apply the distortion correction to one image.
#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
I have created a function for this purpose named pipeline() referenced by `# ref_03_pipeline` tag

I used a combination of color and gradient thresholds to generate a binary image.

I have tuned my pipeline on the image from the training materials because it
contains area with bright light and shadow.

This is the result:

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp()`, witch can be located using the `#ref_07_worp` tag
The `warp()` function takes as inputs an image (`img`), and it fortunes the
perspective transform of the image.

The source and destination points are defined in the get_points() function `#ref_05_points`  and the points it returns are hard coded using the following snippet
```
    img_size = (img.shape[1], img.shape[0])
    src = np.float32(
        [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
        [(int(img_size[0] / 6) - 10), img_size[1]],
        [int(img_size[0] * 5 / 6) + 60, img_size[1]],
        [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
    dst = np.float32(
        [[(img_size[0] / 4), 0],
        [(img_size[0] / 4), img_size[1]],
        [(img_size[0] * 3 / 4), img_size[1]],
        [(img_size[0] * 3 / 4), 0]])
```
This resulted in the following source and destination points:
src =  [[  585.   460.]
 [  203.   720.]
 [ 1126.   720.]
 [  695.   460.]]
dst =  [[ 320.    0.]
 [ 320.  720.]
 [ 960.  720.]
 [ 960.    0.]]

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Lines class is the main class in my project when it comes to lane line identification
and polynomial fitting. This class is referenced by #ref_08_lines_class tag.

The Lines.find_lane(image) referenced by #ref_9_find_lane_lines tag is responsible of  
finding lane lines in the processed images. This method takes in an image it
performs the following steps
* it creates a histogram of the image
* it warps the imaged using warp() function
* starting from the bottom it takes a histogram of the half of the image
* based on the value of the histogram I set the window where I have to search for
the left and write lane
* I divide the warped image in 9 horizontal sections and start searching in the
predefined small windows for the lane position
*  If i find at least 50 good pixels in a search the I consider this good pixels
and I set the mean of this pixels as the current position of the lane in that windows
of search
* I fit a second order polynomial to the left points and the write points. (#ref_10_fit_polynomial)

Similar steps I'm doing also in the Lines.fast_find(image) method except
that I'm not taking in the initial histogram of the half of the image
in order to decide where to reach for next line position. I'm using in this search
the previous defined search areas. If I'm not able to find the lanes Then calling
find_lane()


![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

The radius if the curvature is computed by find_curvature() method of the Lanes class referenced
by the #ref_11_radius tag.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in Lines.draw_lines() method referenced by #ref_12_draw_lines.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./output_images/project_result.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Te approach that I took it relies heavily on the instruction notes and code snippets from the course.
The project as it is at the moment it will definitively fail when there are no lane lines available to be identified or when there is only one of them marked or on the road. If I ware going to pursue this project further I will start by addressing this problems first. Also considering
a lane line if very strong curvature that show up curving left and write int the
area where the code is analyzing will cause unpredictable values for the curvature.
