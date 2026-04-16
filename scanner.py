import cv2
import numpy as np
import pyautogui
import keyboard
import os
from smallalgorithms import *

def take_screen():
    a = 0
    while os.path.exists(f'{os.getcwd()}/screenshots/screenshot-{a}.png'):
        a+=1
    keyboard.wait('enter')
    im1 = pyautogui.screenshot()
    im1.save(f"{os.getcwd()}/screenshots/screenshot-{a}.png")

def identify_cells(img,templates,col):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    data = np.empty([1,10])
    for template in templates:
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        filtered = filter(zip(*loc[::-1]),within_10)
        row = 0
        for pt in filtered:
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), col, 1)
            crop = img[pt[1]:pt[1]+h,pt[0]:pt[0]+w]
            np.append(data,crop,row)
        cv2.imwrite('res.png',img)
        row += 1