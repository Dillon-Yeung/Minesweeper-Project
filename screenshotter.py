import pyautogui
import keyboard
import os

def take_screen(num):
    keyboard.wait('enter')
    im1 = pyautogui.screenshot()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    im1.save(os.path.join(screenshots_dir, f"screenshot-{num}.png"))
