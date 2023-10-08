import cv2
import numpy as np

# Load the image
image = cv2.imread('original.png')

# ------------------ Define region of interest -------------------------

# Define the four points for the ROI (the top left corner is 0,0)
roi_vertices = np.array(
    [[(100, 1800), (600, 600), (1200, 600), (1770, 1800)]], dtype=np.int32)

# Mask for ROI
roi_mask = np.zeros_like(image)
cv2.fillPoly(roi_mask, roi_vertices, (255, 255, 255))

# Display the original image
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Draw blue dots at the vertices of the ROI
roi_Points = [(100, 1800), (600, 600), (1200, 600), (1770, 1800)]
for point in roi_Points:
    cv2.circle(image, point, 10, (255, 0, 0), -1)

# Display the image with blue dots in the ROI
cv2.imshow("Dots on ROI Vertices", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Draw the blue dots at the vertices of the ROI on the mask
roi_Points = [(100, 1800), (600, 600), (1200, 600), (1770, 1800)]
for point in roi_Points:
    cv2.circle(roi_mask, point, 10, (255, 0, 0), -1)

# Show the masked area with the blue dots
cv2.imshow("ROI Mask", roi_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# --------------- Find the red cones only within the mask ------------------

# Convert the image to HSV colors
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Show the image after converting to HSV for better color recognition
cv2.imshow("Original Image in HSV Colors", hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Define lower and upper thresholds for first red color
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Create a mask for red color
mask1 = cv2.inRange(hsv, lower_red, upper_red)

# Show red mask merged with ROI mask
masked_roi_1 = cv2.bitwise_and(mask1, roi_mask[:, :, 0])
cv2.imshow("First Red Mask Merged with ROI Mask", masked_roi_1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Define lower and upper thresholds for other red color
lower_red = np.array([160, 100, 100])
upper_red = np.array([180, 255, 255])

# Create a mask for red color (continued)
mask2 = cv2.inRange(hsv, lower_red, upper_red)

# Show red second red mask merged with ROI mask
# need to use [:,:,0] to make sure size of arrays is correct!
masked_roi_2 = cv2.bitwise_and(mask2, roi_mask[:, :, 0])
cv2.imshow("Second Red Mask Merged with ROI Mask", masked_roi_2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Combine both masks to detect red cones within the ROI
mask = mask1 + mask2
masked_roi = cv2.bitwise_and(mask, roi_mask[:, :, 0])

# Display the mask showing the detected red regions in the ROI
cv2.imshow("Combined Red Masks in ROI", masked_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ----------------------- Find contours of cones -----------------------------

# Find contours of red cones within the ROI
contours, _ = cv2.findContours(
    masked_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours on the original image
contour_image = image.copy()  # Create a copy of the original image
cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 2)
cv2.imshow("Contours on Original Image", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ---------------------Assign left and right cones -------------------------

# Create lists to cones on right and left
left_cone_centers = []
right_cone_centers = []

# Draw dots on cones and store their locations
for contour in contours:
    if cv2.contourArea(contour) > 300:  # filter out potential smaller red objects
        moments = cv2.moments(contour)
        if moments['m00'] != 0:  # checks to make sure area is not zero
            # calculate centroid x-coord
            x_coord = int(moments['m10'] / moments['m00'])
            # calculcate centroid y-coord
            y_coord = int(moments['m01'] / moments['m00'])
            if x_coord < image.shape[1] // 2:  # if on left side
                left_cone_centers.append((x_coord, y_coord))
                cv2.circle(image, (x_coord, y_coord), 5, (255, 0, 0), -1)
            else:  # if on right side
                right_cone_centers.append((x_coord, y_coord))
                cv2.circle(image, (x_coord, y_coord), 5, (0, 255, 0), -1)

# Display the image with dots on detected cones
cv2.imshow("Dots on Detected Cones", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ----------------Fitting lines to cones --------------------

# Fit a line to the left cones
if len(left_cone_centers) >= 2:
    left_cone_centers = np.array(left_cone_centers)
    # asking for 50% of points to be on line and 30% accuracy
    left_line = cv2.fitLine(left_cone_centers, cv2.DIST_L2, 0, 0.50, 0.30)
    x_dir = left_line[0][0]
    y_dir = left_line[1][0]
    x = left_line[2][0]
    y = left_line[3][0]
    width = image.shape[1]
    height = image.shape[0]

    # bottom left point
    x1 = int(x+x_dir*((height-y)/y_dir))
    y1 = height

    # top left point
    x2 = int(x+x_dir*(-y/y_dir))
    y2 = 0

    # draw line on image
    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
else:
    print("Not enough points to generate line for left side")

# Fit a line to the right cones
if len(right_cone_centers) >= 2:
    right_cone_centers = np.array(right_cone_centers)
    # asking for 50% of points to be on line and 30% accuracy
    right_line = cv2.fitLine(right_cone_centers, cv2.DIST_L2, 0, 0.50, 0.30)

    x_dir = right_line[0][0]
    y_dir = right_line[1][0]
    x = right_line[2][0]
    y = right_line[3][0]
    width = image.shape[1]
    height = image.shape[0]

    # bottom right point
    x1 = int(x+x_dir*((height-y)/y_dir))
    y1 = height

    # top right point
    x2 = int(x+x_dir*(-y/y_dir))
    y2 = 0

    # draw line on image
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
else:
    print("Not enough points to generate line for left side")


# Display the final image with fitted lines
cv2.imshow("Detected Lines", image)
cv2.imwrite("output.png", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
