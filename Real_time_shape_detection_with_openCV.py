#After setting the HSV values ​​of the color of the shape you selected in the trackbar, show it to the camera

import cv2
import numpy as np

# Open a video capture object for the default camera (index 0)
cap = cv2.VideoCapture(0)

# Set the font for drawing text
font = cv2.FONT_HERSHEY_SIMPLEX

# Callback function for trackbar
def nothing(x):
    pass

# Create a window for trackbars and set its size
cv2.namedWindow("trackbar")
cv2.resizeWindow("trackbar", 500, 500)

# Create trackbars for lower HSV values
cv2.createTrackbar("Lower-H", "trackbar", 0, 180, nothing)
cv2.createTrackbar("Lower-S", "trackbar", 0, 255, nothing)
cv2.createTrackbar("Lower-V", "trackbar", 0, 255, nothing)

# Create trackbars for upper HSV values
cv2.createTrackbar("Upper-H", "trackbar", 0, 180, nothing)
cv2.createTrackbar("Upper-S", "trackbar", 0, 255, nothing)
cv2.createTrackbar("Upper-V", "trackbar", 0, 255, nothing)

# Set initial upper HSV values to maximum
cv2.setTrackbarPos("Upper-H", "trackbar", 180)
cv2.setTrackbarPos("Upper-S", "trackbar", 255)
cv2.setTrackbarPos("Upper-V", "trackbar", 255)

# Main loop for video processing
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame from BGR to HSV color space
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current lower HSV values from trackbars
    lower_h = cv2.getTrackbarPos("Lower-H", "trackbar")
    lower_s = cv2.getTrackbarPos("Lower-S", "trackbar")
    lower_v = cv2.getTrackbarPos("Lower-V", "trackbar")

    # Get current upper HSV values from trackbars
    upper_h = cv2.getTrackbarPos("Upper-H", "trackbar")
    upper_s = cv2.getTrackbarPos("Upper-S", "trackbar")
    upper_v = cv2.getTrackbarPos("Upper-V", "trackbar")

    # Define lower and upper HSV color ranges
    lower_color = np.array([lower_h, lower_s, lower_v])
    upper_color = np.array([upper_h, upper_s, upper_v])

    # Create a binary mask based on the HSV color range
    mask = cv2.inRange(frame_hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    for cnt in contours:
        # Approximate the contour with polygonal curves
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Draw the contours on the original frame
        cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

        # Get the coordinates of the first point in the contour
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        # Classify and label the shapes based on the number of vertices
        if len(approx) == 3:
            cv2.putText(frame, "Triangle", (x - 50, y), font, 1, (0))
        elif len(approx) == 4:
            cv2.putText(frame, "Rectangle", (x - 50, y), font, 1, (0))
        elif len(approx) == 5:
            cv2.putText(frame, "Pentagon", (x - 50, y), font, 1, (0))
        elif len(approx) == 6:
            cv2.putText(frame, "Hexagon", (x - 50, y), font, 1, (0))
        else:
            cv2.putText(frame, "Ellipse", (x - 50, y), font, 1, (0))

    # Display the original frame and the masked image
    cv2.imshow("original", frame)
    cv2.imshow("masked", mask)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
