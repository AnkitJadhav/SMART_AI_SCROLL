import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
black_low = np.array([0,50,50])
black_high = np.array([10,255,255])

yellow_low = np.array([23,93,0])
yellow_high = np.array([45,255,255])
prev_y = 0
prey_x = 0
run = True
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, yellow_low, yellow_high)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 300:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            if y < prev_y:
                pyautogui.press('down')
            prev_y = y

    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, black_low, black_high)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 300:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            if x < prey_x:
                pyautogui.press('up')
            prey_x = x

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()