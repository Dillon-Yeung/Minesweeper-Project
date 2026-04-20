import numpy as np
import cv2
import os
from scanner_local import identify_cells
    
def get_files_from(folder):
    return os.listdir(folder)

def train_knn():
    data = []
    responses = []
    files = get_files_from(f"{os.getcwd()}/auto")
    index_data = {}
    for file in files:
        if not file.endswith('.png'):
            continue
        parts = file.split("_")
        if len(parts) < 3:
            continue
        try:
            index = int(parts[1])
        except (ValueError, IndexError):
            continue
        img = cv2.imread(f"{os.getcwd()}/auto/{file}", cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        if index not in index_data:
            index_data[index] = []
        index_data[index].append(img)
    for index, imgs in index_data.items():
        for img in imgs:
            resized = cv2.resize(img, (20, 20))
            flat_img = resized.flatten().astype('float32')
            data.append(flat_img)
            responses.append(index)
    data = np.array(data, dtype=np.float32)
    responses = np.array(responses, dtype=np.int32)
    knn = cv2.ml.KNearest_create()
    knn.train(data, cv2.ml.ROW_SAMPLE, responses)
    return knn

test_case1 = cv2.imread('screenshots/screenshot-22.png')
assert test_case1 is not None
test_case2 = cv2.imread('screenshots/screenshot-14.png')
assert test_case2 is not None
test_case3 = cv2.imread('screenshots/screenshot-23.png')
covered = cv2.imread('compare/cover.png',cv2.IMREAD_GRAYSCALE)
assert covered is not None
empty = cv2.imread('compare/empty.png',cv2.IMREAD_GRAYSCALE)
assert empty is not None
one = cv2.imread('compare/1.png',cv2.IMREAD_GRAYSCALE)
assert one is not None
two = cv2.imread('compare/2.png',cv2.IMREAD_GRAYSCALE)
assert two is not None
three = cv2.imread('compare/3.png',cv2.IMREAD_GRAYSCALE)
assert three is not None
four = cv2.imread('compare/4.png',cv2.IMREAD_GRAYSCALE)
assert four is not None
five = cv2.imread('compare/5.png',cv2.IMREAD_GRAYSCALE)
assert five is not None
six = cv2.imread('compare/6.png',cv2.IMREAD_GRAYSCALE)
assert six is not None
seven = cv2.imread('compare/7.png',cv2.IMREAD_GRAYSCALE)
assert seven is not None
eight = cv2.imread('compare/8.png',cv2.IMREAD_GRAYSCALE)
assert eight is not None


def test(test_case,rows,cols):
    img = identify_cells(test_case,(covered,empty,one,two,three,four,five,six,seven,eight))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = []
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    h, w = thresh.shape

    cell_h = h // rows
    cell_w = w // cols

    cells = []

    for i in range(rows):
        for j in range(cols):
            cell = thresh[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            cells.append(cell)

    def preprocess_cell(cell):
        resized = cv2.resize(cell, (20, 20))
        flattened = resized.reshape(-1).astype('float32')
        return flattened


    for cell in cells:
        sample = preprocess_cell(cell)
        sample = sample.reshape(1, -1)
        result = train_knn().findNearest(sample, k=1)[1]
        results.append(int(result[0][0])-2)

    board = np.array(results).reshape(rows, cols)
    print(board)
    print("Done")

test(test_case3,2,2)
test(test_case1,16,30)
