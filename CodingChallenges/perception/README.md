#Perception Challenge
## Description
This script takes in an image, uses opencv to identify red cones within the image, and draws two lines of best fit along the cones.
One line will be on the left side of the image and the other will be on the right side. It is intended to be used on an image where the cones represent lane lines for a theoretical vehicle.
The program will visualize some of the image processing done and will output a "output.png" file upon termination.

## Setup
run "pip3 install opencv-python"

## Controls
Press any key to continue through the program. The program ends on the last keystroke.

## Implementation
- mask is used to define a region of interst (ROI)
- image is converted to HSV colors for better color detection
- image is masked using color thresholds
- color masks and and region of interst mask are merged
- contour lines are found based on the merged mask
- centroids of contour lines are found
- some math is used to find endpoints of the lines of best fit
