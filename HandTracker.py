import cv2
import mediapipe as mp
import time
import math
from math import atan2, degrees
from switchcase import switch

# List of tip landmarks for each finger
tips = [4, 8, 12, 16, 20]

class handDetector():
    def __init__(self, mode=False, maxH=2, dCon=0.5, dTac=0.5):
        # Initialize hand detector with parameters
        self.mode = mode  # Static image mode or not
        self.maxH = maxH  # Maximum number of hands to detect
        self.dCon = dCon  # Minimum detection confidence
        self.dTac = dTac  # Minimum tracking confidence

        # Initialize MediaPipe hands solution
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, max_num_hands=self.maxH, min_detection_confidence=self.dCon, min_tracking_confidence=self.dTac)
        self.mpDraw = mp.solutions.drawing_utils  # Utility for drawing landmarks
        self.orient = ""  # Orientation of hand

    def find_hands(self, img):
        # Detect hands in the input image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
        self.results = self.hands.process(imgRGB)  # Process the image to detect hands
        self.img = img
        img = imgRGB
        return img

    def find_position(self, img, i, handNo=0, draw=True):
        # Find the positions of landmarks for a specific hand
        x = []
        y = []
        box = []
        self.positions = []  # Store landmark positions

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]  # Get landmarks for the specified hand
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert normalized coordinates to pixel values
                x.append(cx)
                y.append(cy)
                self.positions.append([id, cx, cy])  # Append landmark ID and coordinates
                if draw:
                    self.mpDraw.draw_landmarks(i, hand, self.mpHands.HAND_CONNECTIONS)  # Draw landmarks and connections
            box = [min(x), min(y), max(x), max(y)]  # Calculate bounding box around hand
            if draw:
                cv2.rectangle(i, (box[0] - 20, box[1] - 20), (box[2] + 20, box[3] + 20), (0, 255, 0), 2)  # Draw bounding box

    def find_orientation(self, xy1, xy2):
        # Determine the orientation of the hand
        try:
            if len(self.positions) != 0:
                self.orient = ""
                angle = degrees(atan2(xy2[2] - xy1[2], xy1[1] - xy2[1]))  # Calculate angle between two points
                if angle < 0:
                    angle += 360
                if 45 <= angle <= 135:
                    self.orient = "Up"
                elif 135 <= angle <= 225:
                    self.orient = "Left"
                elif 225 <= angle <= 315:
                    self.orient = "Down"
                elif angle >= 315 or angle <= 45:
                    self.orient = "Right"
                    return self.orient
        except:
            pass

    def find_position_screen(self, img, w, h, handNo=0):
        # Map hand positions to screen dimensions
        self.w = w
        self.h = h
        self.screenPositions = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * self.w), int(lm.y * self.h)  # Scale normalized coordinates to screen size
                self.screenPositions.append([id, cx, cy])

    def find_open_fingers(self, ot=False):
        # Determine which fingers are open
        self.open_fingers = []
        x = True
        if len(self.positions) != 0:
            if not ot:  # Default orientation
                if self.positions[3][1] < self.positions[17][1]:
                    x = True
                if self.positions[3][1] > self.positions[17][1]:
                    x = False
                self.open_fingers = []
                if x:
                    if self.positions[tips[0]][1] < self.positions[tips[0] - 1][1]:
                        self.open_fingers.append(1)  # Thumb is open
                    else:
                        self.open_fingers.append(0)  # Thumb is closed
                elif not x:
                    if self.positions[tips[0]][1] > self.positions[tips[0] - 1][1]:
                        self.open_fingers.append(1)
                    else:
                        self.open_fingers.append(0)

                for i in range(1, 5):
                    if self.positions[tips[i]][2] < self.positions[tips[i] - 2][2]:
                        self.open_fingers.append(1)  # Finger is open
                    else:
                        self.open_fingers.append(0)  # Finger is closed
            elif ot:  # Orientation-based logic
                for case in switch(self.orient):
                    if case("Up"):
                        # Logic for fingers open when hand is oriented upwards
                        pass
                    if case("Down"):
                        # Logic for fingers open when hand is oriented downwards
                        pass
                    if case("Left"):
                        # Logic for fingers open when hand is oriented to the left
                        pass
                    if case("Right"):
                        # Logic for fingers open when hand is oriented to the right
                        pass

    def find_distance(self, i, a, b, draw=True):
        # Calculate distance between two landmarks
        if len(self.positions) != 0:
            if draw:
                x1, y1 = self.positions[a][1], self.positions[a][2]
                x2, y2 = self.positions[b][1], self.positions[b][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(i, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # Draw circle at first point
                cv2.circle(i, (x2, y2), 15, (255, 0, 255), cv2.FILLED)  # Draw circle at second point
                cv2.circle(i, (cx, cy), 15, (255, 0, 255), cv2.FILLED)  # Draw circle at midpoint
                cv2.line(i, (x1, y1), (x2, y2), (255, 0, 255), 3)  # Draw line between points

                self.len = math.hypot(x2 - x1, y2 - y1)  # Calculate Euclidean distance


