import os
import cv2
import numpy as np
def filter(data, condition):
    result = []
    for element in data:
        if all(condition(element, existing) for existing in result):
            result.append(element)
    return result

def within_10(d1,d2):
    return abs(d1[0]-d2[0]) > 10 or abs(d1[1]-d2[1]) > 10



