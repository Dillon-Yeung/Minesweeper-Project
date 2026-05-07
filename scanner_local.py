import cv2
import numpy as np
import os
from screen import filter, within_10

def identify_cells(img,templates):
    img_draw = img.copy()
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    auto_dir = os.path.join(os.path.dirname(__file__), 'auto')
    if not os.path.exists(auto_dir):
        os.makedirs(auto_dir)
    for filename in os.listdir(auto_dir):
        path = os.path.join(auto_dir, filename)
        if os.path.isfile(path):
            os.remove(path)
    for template_index, template in enumerate(templates, start=0):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where( res >= threshold)
        filtered = list(filter(zip(*loc[::-1]),within_10))
        counter = 0
        for pt in filtered:
            counter +=1
            crop = img[(pt[1]):(pt[1]+h),(pt[0]):(pt[0]+w)]
            filename = os.path.join(
                auto_dir,
                f"autoscreenshot_{template_index}_{counter}.png"
            )
            cv2.imwrite(filename, crop)
        cv2.imwrite('res.png',img_draw)
    if filtered:
        xs, ys = zip(*filtered)
        return img[min(ys):max(ys), min(xs):max(xs)]
    else:
        return img



