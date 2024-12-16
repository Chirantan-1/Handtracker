import cv2
import time
import HandTracker as htm
import numpy as np
from math import atan2, degrees
import serial
import time


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
tips = [4, 8, 12, 16, 20]
cap.set(3, 800)
cap.set(4, 800)
i = 0
line = []
command = "OFF"

detector = htm.handDetector(dCon=0.75)

try:
    s = serial.Serial(port = "COM9", baudrate = 9600)
    time.sleep(2)
except:
    pass
while True: 
    i += 1
    x, img = cap.read()
    img = cv2.flip(img, 1)
    try:
        h, w, _ = img.shape
    except:
        pass
    image = np.zeros((h, w, 3), np.uint8)
#    image = img
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    img = detector.find_hands(img)
    detector.find_position(img, image)
    list = detector.positions
    detector.find_open_fingers(ot=True)
    #detector.find_distance(img, image, 8, 4)
    
    n = 0

    if(detector.open_fingers == [0, 0, 0, 0, 0]):
        n = 0
        command = b"OFF"
    elif(detector.open_fingers == [0, 1, 0, 0, 0]):
        n = 1
    elif(detector.open_fingers == [0, 1, 1, 0, 0]):
        n = 2
        line.append(list[8])
    elif(detector.open_fingers == [0, 1, 1, 1, 0]):
        line = []
        n = 3
    elif(detector.open_fingers == [0, 1, 1, 1, 1]):
        n = 4
    elif(detector.open_fingers == [1, 1, 1, 1, 1]):
        n = 5
        command = b"ON"
    elif(detector.open_fingers == [1, 0, 0, 0, 0]):
        n = 6
    elif(detector.open_fingers == [1, 1, 0, 0, 0]):
        n = 7
    elif(detector.open_fingers == [1, 1, 1, 0, 0]):
        n = 8
    elif(detector.open_fingers == [1, 1, 1, 1, 0]):
        n = 9
    if (i % 25) == 0:
        try:
            s.write(command)
            print("ok")
        except:
            pass

#    print(line_orientation(list[0][1:], list[9][1:]))
    if(len(list) != 0):
        detector.find_orientation(list[9], list[0])
    print(detector.open_fingers)
        #print(detector.open_fingers)
#    for h in line:
#        cv2.circle(image, h[1:], 15, (255, 255, 255), cv2.FILLED)
    cv2.putText(image, str(int(n)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    cv2.imshow("Image", image)
    cv2.imshow("Image2", img)
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
#    print(detector.orient)
#    print(time.time())