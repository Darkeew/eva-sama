import cv2
import numpy as np
import pyautogui


def rating(coords, template):
    image = pyautogui.screenshot(region=(coords))
    image = np.array(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0,0,0])
    upper = np.array([0,0,0])
    mask = cv2.inRange(hsv, lower, upper)
    image = 255 - mask
    cv2.imshow('test', image)
    cv2.waitKey(1)
    rating = np.sum(image == 0)
    if template == 'karaoke':
        if rating > 200:
            return True
        else:
            return False
    else:
        if rating == 0:
            return True
        else:
            return False
