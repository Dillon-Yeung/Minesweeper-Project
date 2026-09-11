import pyautogui
import keyboard
import os

def take_screen(num):
    keyboard.wait('enter')
    im1 = pyautogui.screenshot()
    im1.save(f"{os.getcwd()}/screenshots/screenshot-{num}.png")
