import cv2
import numpy as np
import HandTracker as htm
from pynput.mouse import Controller, Button

mouse = Controller()

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
detector = htm.handDetector(maxH=1)
x, img = cap.read()
img = cv2.flip(img, 1)
h, w, c = img.shape
image = np.zeros((h, w, 3), np.uint8)
plocx, plocy = 0, 0
clocx, clocy = 0, 0

ws, hs = 1920, 1080  

while True:
    x, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    detector.find_position(img, image)
    detector.find_open_fingers()
    list = detector.positions

    if len(list) != 0:
        x1, y1 = list[8][1:]
        x2, y2 = list[12][1:]
        detector.find_orientation(list[9], list[0])
        detector.find_open_fingers(ot=True)
        cv2.rectangle(image, (100, 100), (768, 432), (255, 0, 255), 2)

        fingers = detector.open_fingers
        print(fingers)
        if fingers[4] != 1:
            if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
                x3 = np.interp(x1, (100, 768), (0, ws))
                y3 = np.interp(y1, (100, 432), (0, hs))

                clocx = plocx + (x3 - plocx) / 5
                clocy = plocy + (y3 - plocy) / 5
                try:
                    mouse.position = (clocx, clocy)
                except:
                    pass
                print(x3, y3)
                cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocx, plocy = clocx, clocy
            elif fingers[1] == 1 and fingers[2] == 1:
                detector.find_distance(image, 8, 12)
                if detector.len <= 40:
                    cv2.circle(image, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(image, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                    if fingers[3] == 0:
                        mouse.click(Button.left)
                    elif fingers[3] == 1:
                        mouse.click(Button.right)

    cv2.imshow("Image", image)
    cv2.imshow("Image2", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    image = np.zeros((h, w, 3), np.uint8)
