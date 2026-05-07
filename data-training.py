import numpy as np
import cv2
import os
from scanner_local import identify_cells

np.set_printoptions(linewidth=100)

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
        img = load_img(f"{os.getcwd()}/auto/{file}", cv2.IMREAD_GRAYSCALE)
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

def load_img(path, type=None):
    if type is not None:
        img = cv2.imread(path, type)
    else:
        img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Missing image: {path}")
    return img

test_case1 = load_img('screenshots/screenshot-13.png')
test_case2 = load_img('screenshots/screenshot-14.png')
test_case3 = load_img('screenshots/screenshot-23.png')
covered = load_img('compare/.online/cover.png', cv2.IMREAD_GRAYSCALE)
empty = load_img('compare/.online/empty.png', cv2.IMREAD_GRAYSCALE)
one = load_img('compare/.online/1.png', cv2.IMREAD_GRAYSCALE)
two = load_img('compare/.online/2.png', cv2.IMREAD_GRAYSCALE)
three = load_img('compare/.online/3.png', cv2.IMREAD_GRAYSCALE)
four = load_img('compare/.online/4.png', cv2.IMREAD_GRAYSCALE)
five = load_img('compare/.online/5.png', cv2.IMREAD_GRAYSCALE)
six = load_img('compare/.online/6.png', cv2.IMREAD_GRAYSCALE)
seven = load_img('compare/.online/7.png', cv2.IMREAD_GRAYSCALE)
eight = load_img('compare/.online/8.png', cv2.IMREAD_GRAYSCALE)


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


    samples = []
    for cell in cells:
        sample = preprocess_cell(cell)
        samples.append(sample)
    
    samples_array = np.array(samples, dtype=np.float32).reshape(len(samples), -1)
    results = train_knn().findNearest(samples_array, k=1)[1].flatten()
    results = [int(r) - 2 for r in results]

    board = np.array(results).reshape(rows, cols)
    print(board)
    print("Done")

test(test_case3,2,2)
test(test_case1,16,30)
