import cv2
import numpy as np

# Read an image from file
img = cv2.imread("polygons.png")

# Set the font for drawing text
font = cv2.FONT_HERSHEY_SIMPLEX

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through each contour
for cnt in contours:
    # Approximate the contour with polygonal curves
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    # Draw the contours on the original image
    cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)

    # Calculate the centroid of the contour
    moments = cv2.moments(approx)
    x = int(moments["m10"] / moments["m00"])
    y = int(moments["m01"] / moments["m00"])

    # Classify and label the shapes based on the number of vertices
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x - 50, y), font, 1, (0))
    elif len(approx) == 4:
        cv2.putText(img, "Rectangle", (x - 50, y), font, 1, (0))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x - 50, y), font, 1, (0))
    elif len(approx) == 6:
        cv2.putText(img, "Hexagon", (x - 50, y), font, 1, (0))
    else:
        cv2.putText(img, "Ellipse", (x - 50, y), font, 1, (0))

# Display the annotated image
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
