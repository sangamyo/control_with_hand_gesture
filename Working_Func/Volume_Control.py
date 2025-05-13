import os
import math
import cv2
import mediapipe as mp
import numpy as np

# Mediapipe API
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# macOS Volume Control Function
def set_volume_mac(volume_percentage):
    """Set system volume on macOS."""
    volume_level = int(volume_percentage / 100 * 7)  # macOS volume is from 0 to 7
    os.system(f"osascript -e 'set volume output volume {volume_level * 14.3}'")

# Video Capture
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        results = hands.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        lmList = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get coordinates of thumb and index finger
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Calculate the distance between thumb and index finger
            d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            # Set volume based on the distance
            volume_percentage = np.interp(d, [50, 270], [0, 100])
            set_volume_mac(volume_percentage)

            # Draw UI elements
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            cv2.putText(img, f'Volume: {int(volume_percentage)}%', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('Volume Controller', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
