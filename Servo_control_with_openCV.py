#servo moves according to the position of the hand

import cv2
from cvzone.HandTrackingModule import HandDetector
from pyfirmata import Arduino, SERVO
from time import sleep

# Specify the COM port for Arduino
port = 'COM7'

# Specify the pin for the bottom servo motor
pin_bottom_servo = 3

# Initialize Arduino board and configure servo motor
board = Arduino(port)
board.digital[pin_bottom_servo].mode = SERVO


# Function to rotate the servo motor to a specified angle
def rotate_servo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)


# Open a video capture object for the default camera (index 0)
cap = cv2.VideoCapture(0)

# Create a hand detector object
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    # Read a frame from the video capture
    ret, img = cap.read()

    # Flip the frame horizontally
    img = cv2.flip(img, 1)

    # Detect hands in the frame
    hands, img = detector.findHands(img, flipType=False)

    # Draw reference lines on the image
    cv2.line(img, (285, 0), (285, 480), (0, 0, 255), thickness=2)
    cv2.line(img, (355, 0), (355, 480), (0, 0, 255), thickness=2)
    cv2.line(img, (0, 240), (640, 240), (0, 0, 255), thickness=2)

    # Process each detected hand
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerpoint1 = hand1["center"]
        handType1 = hand1["type"]

        # Draw a circle at the center of Hand 1
        cv2.circle(img, centerpoint1, 10, (0, 0, 255), -1)

        # Calculate the angle for the bottom servo based on Hand 1 position
        #because of the frame's resolution(640,480) max angle = (640-355)/1.6 = 178 degree
        bottom_angle = int((centerpoint1[0] - 355) / 1.6)

        # Rotate the bottom servo to the calculated angle
        rotate_servo(pin_bottom_servo, bottom_angle)

        # Check if there are two hands
        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerpoint2 = hand2["center"]
            handType2 = hand2["type"]

            # Draw a circle at the center of Hand 2
            cv2.circle(img, centerpoint2, 10, (0, 0, 255), -1)

    # Display the annotated image
    cv2.imshow("image", img)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
