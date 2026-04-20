import os
import cv2
import numpy as np

o_covered = cv2.imread('compare/.online/cover.png',cv2.IMREAD_GRAYSCALE)
assert o_covered is not None
o_empty = cv2.imread('compare/.online/empty.png',cv2.IMREAD_GRAYSCALE)
assert o_empty is not None
o_one = cv2.imread('compare/.online/one.png',cv2.IMREAD_GRAYSCALE)
assert o_one is not None
o_two = cv2.imread('compare/.online/two.png',cv2.IMREAD_GRAYSCALE)
assert o_two is not None
o_three = cv2.imread('compare/.online/three.png',cv2.IMREAD_GRAYSCALE)
assert o_three is not None
o_four = cv2.imread('compare/.online/four.png',cv2.IMREAD_GRAYSCALE)
assert o_four is not None
o_five = cv2.imread('compare/.online/five.png',cv2.IMREAD_GRAYSCALE)
assert o_five is not None
o_six = cv2.imread('compare/.online/six.png',cv2.IMREAD_GRAYSCALE)
assert o_six is not None
o_seven = cv2.imread('compare/.online/seven.png',cv2.IMREAD_GRAYSCALE)
assert o_seven is not None
o_eight = cv2.imread('compare/.online/eight.png',cv2.IMREAD_GRAYSCALE)
assert o_eight is not None


def identify_cells(img,templates):
    img_draw = img.copy()
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    auto_dir = os.path.join(os.path.dirname(__file__), 'auto')
    for filename in os.listdir(auto_dir):
        path = os.path.join(auto_dir, filename)
        if os.path.isfile(path):
            os.remove(path)
    for template_index, template in enumerate(templates, start=1):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.85
        loc = np.where( res >= threshold)
        filtered = filter(zip(*loc[::-1]),within_10)
        counter = 0
        for pt in filtered:
            counter +=1
            crop = img[(pt[1]):(pt[1]+h),(pt[0]):(pt[0]+w)]
            filename = os.path.join(
                r"C:\Users\dillo\OneDrive\Desktop\Code\auto",
                f"autoscreenshot-{template_index-1}-{counter}.png"
            )
            cv2.imwrite(filename, crop)
        cv2.imwrite('result.png',img_draw)
        cv2.waitKey(1)
        cv2.destroyAllWindows()

def get_files_from(folder):
    return os.listdir(folder)

def train_knn():
    data = []
    labels = []
    files = get_files_from(f"{os.getcwd()}/auto")
    index_data = {}
    for file in files:
        parts = file.split("-")
        index = int(parts[1])
        img = cv2.imread(f"{os.getcwd()}/auto/{file}", cv2.IMREAD_GRAYSCALE)
        assert img is not None
        index_data[index] = img.flatten()
    for index, imgs in index_data.items():
        for flat_img in imgs:
            data.append(flat_img)
            labels.append(index)
    data = np.array(data, dtype=np.float32)
    labels = np.array(labels, dtype=np.int32)
    knn = cv2.ml.KNearest_create()
    knn.train(data, cv2.ml.ROW_SAMPLE, labels)
    np.savez('.online.npz', training=data,labels=labels)
    return knn

train_knn().