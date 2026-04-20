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

