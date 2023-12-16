import cv2
from cvzone.HandTrackingModule import HandDetector
from pyfirmata import Arduino ,SERVO,util
from time import sleep

#the Port that Arduino connected
port = 'COM2'

#Servo Pins
pin_bottom_servo = 9
pin_right_servo = 3
pin_left_servo = 6
pin_clamp_servo = 5

#Servo Degrees, started with 90 degree
bottom_degree = 90
right_degree = 90
left_degree=90
clamp_degree=90

#initializes and configures servo motor pins on Arduino
board = Arduino(port)
board.digital[pin_bottom_servo].mode = SERVO
board.digital[pin_right_servo].mode = SERVO
board.digital[pin_left_servo].mode = SERVO
board.digital[pin_clamp_servo].mode = SERVO


#function that rotates Servos
def rotateservo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.012)


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8,maxHands=2)

#servos are adjusted to 90 degrees before the camera is turned on
rotateservo(pin_left_servo,left_degree)
rotateservo(pin_right_servo,right_degree)
rotateservo(pin_bottom_servo,bottom_degree)
rotateservo(pin_clamp_servo,clamp_degree)

while True:
    ret,img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img,flipType=False)

    if hands:
       #hand1
       hand1 = hands[0]
       lmList1 = hand1["lmList"]
       bbox1 = hand1["bbox"]
       handType1 = hand1["type"]
       fingers1 = detector.fingersUp(hand1)

       if len(hands) == 2:
           # hand2
           hand2 = hands[1]
           lmList2 = hand2["lmList"]
           bbox2 = hand2["bbox"]
           handType2 = hand2["type"]
           fingers2 = detector.fingersUp(hand2)

           # right hand thumb moves the bottom servo to right
           if fingers1 == [0, 0, 0, 0, 0]:
               if bottom_degree >0:
                   bottom_degree = bottom_degree - 3
                   rotateservo(pin_bottom_servo, bottom_degree)
               else:
                   print("reached min")
               pass

           # left hand thumb moves the bottom servo to left
           if fingers2 == [0, 0, 0, 0, 0]:
               if bottom_degree <180:
                   bottom_degree = bottom_degree + 3
                   rotateservo(pin_bottom_servo, bottom_degree)
               else:
                   print("reached max")
               pass


           #four sign made with the right hand activates the left servo and lifts the arm up.
           if fingers1 == [1, 1, 1, 1, 1]:
               if left_degree > 0:
                   left_degree = left_degree - 3
                   rotateservo(pin_left_servo, left_degree)
               else:
                   print("Reached min")
               pass

           #four sign made with the left hand activates the left servo and lifts the arm down.
           if fingers2 == [1, 1, 1, 1, 1]:
               if left_degree <180 :
                   left_degree = left_degree + 3
                   rotateservo(pin_left_servo, left_degree)
               else:
                   print("Reached max")
               pass


           # two sign made with the right hand's forefinger and middlefinger activates the right servo and then arm goes forward.
           if fingers1 == [1, 1, 1, 0, 0]:
               if right_degree>0:
                   right_degree = right_degree-3
                   rotateservo(pin_right_servo,right_degree)
               else:
                   print("Reached min")
               pass

           #two sign made with the left hand's forefinger and middlefinger activates the right servo and then arm goes backward
           if fingers2 == [1, 1, 1, 0, 0]:
               if right_degree < 180:
                   right_degree = right_degree + 3
                   rotateservo(pin_right_servo, right_degree)
               else:
                   print("Reached max")
               pass

           #If we open the thumb and forefinger of the right hand, the clamp opens.
           if fingers1 == [0, 1, 0, 0, 0]:
               if clamp_degree>0:
                   clamp_degree = clamp_degree-3
                   rotateservo(pin_clamp_servo,clamp_degree)
               else:
                   print("Reached min")
               pass

           #If we open the thumb and forefinger of the left hand, the clamp closes.
           if fingers2 == [0, 1, 0, 0, 0]:
               if clamp_degree < 180:
                   clamp_degree = clamp_degree + 3
                   rotateservo(pin_clamp_servo, clamp_degree)
               else:
                   print("Reached max")
               pass

    cv2.imshow("image",img)
    #if we press q then the code stops running
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()