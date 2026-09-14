import cv2
import numpy as np
import os
import logging
from screen import deduplicate_points

logger = logging.getLogger(__name__)

DEFAULT_KNN_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "knn_model.xml"
)

DEFAULT_TRAINING_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "knn_training_data.npz"
)

TEMPLATE_LABEL_MAP = {
    1: -1,   # covered
    2: 0,    # empty
    3: 1,    # one
    4: 2,    # two
    5: 3,    # three
    6: 4,    # four
    7: 5,    # five
    8: 6,    # six
    9: 7,    # seven
    10: 8,   # eight
    11: 10,  # flag 
}

def build_training_data(cell_matches, img_gray, templates):
    rep_h, rep_w = templates[0].shape

    samples = []
    labels = []

    for x, y, template_index, confidence in cell_matches:
        patch = img_gray[y:y + rep_h, x:x + rep_w]

        pad_h = rep_h - patch.shape[0]
        pad_w = rep_w - patch.shape[1]
        if pad_h > 0 or pad_w > 0:
            if patch.shape[0] == 0 or patch.shape[1] == 0:
                continue
            patch = np.pad(patch, ((0,pad_h),(0,pad_w)),mode = 'edge')

        samples.append(patch.flatten().astype(np.float32))
        labels.append(template_index)

    if not samples:
        return(
            np.empty((0,rep_h*rep_w),dtype=np.float32),
            np.empty((0,),dtype=np.int32)
        )
    return np.array(samples,dtype=np.float32),np.array(labels,dtype=np.int32)

def load_training_data(data_path=DEFAULT_TRAINING_DATA_PATH):
    if not os.path.exists(data_path):
        return np.empty((0,0),dtype=np.float32), np.empty((0,),dtype=np.int32)

    data = np.load(data_path)
    return data["samples"], data["labels"]

def accumulate_training_data(samples,labels,data_path=DEFAULT_TRAINING_DATA_PATH):
    existing_samples, existing_labels = load_training_data(data_path)

    if existing_samples.size and existing_samples.shape[1] != samples.shape[1]:
        raise ValueError(f"Feature length mismatch: existing data has "
                         f"{existing_samples.shape[1]} features/sample, new data has "
                         f"{samples.shape[1]}. Are these from templates of different sizes?")

    if existing_samples.size:
        all_samples=np.vstack([existing_samples,samples])
        all_labels=np.concatenate([existing_labels,labels])
    else:
        all_samples=samples
        all_labels=labels

    np.savez(data_path,samples=all_samples,labels=all_labels)
    logger.info(
        "Training data accumulated: %d total samples (%d new this run), saved to %s",
        len(all_labels),len(labels),data_path,
    )
    return all_samples,all_labels

def build_model_from_accumulated_data(data_path=DEFAULT_TRAINING_DATA_PATH,model_output_path=DEFAULT_KNN_MODEL_PATH):
    samples, labels = load_training_data(data_path)
    if len(samples) == 0:
        raise ValueError("No accumulated training data found at {data_path}.")
    knn = train_knn_model(samples,labels)
    save_knn_model(knn, model_output_path)
    return knn

def train_knn_model(samples,label):
    knn=cv2.ml.KNearest_create()
    knn.train(samples,cv2.ml.ROW_SAMPLE,label)
    return knn

def save_knn_model(knn,output_path=DEFAULT_KNN_MODEL_PATH):
    knn.save(output_path)
    logger.info("KNN model saved to %s",output_path)
    return output_path

def load_knn_model(model_path=DEFAULT_KNN_MODEL_PATH):
    return cv2.ml.KNearest_load(model_path)

def classify_cell_knn(knn,patch,k=3,max_distance=None):
    if knn is None:
        return None

    sample = patch.flatten().astype(np.float32).reshape(1,-1)
    retval, results, neighbours, dist = knn.findNearest(sample,k)

    if max_distance is not None and float(dist[0][0]) > max_distance:
        return None
    
    return int(results[0][0])
    
def identify_cells(img,templates,threshold = 0.9,knn_model_path=DEFAULT_KNN_MODEL_PATH,training_data_path=DEFAULT_TRAINING_DATA_PATH):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    cell_matches = [] # stores x, y, index, confidence
    match_results = [] # stores index, result_matrix

    for template_index, template in enumerate(templates, start=1):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        match_results.append((template_index,template,res))
        loc = np.where(res>=threshold)
        filtered = deduplicate_points(zip(*loc[::-1]))

        logger.info(
            "Template %d: %d matches found (after dedupe)",
            template_index, len(filtered),
        )

        if len(filtered) > 1000:
            logger.warning(
                "Template %d: %d matches exceeds sanity cap (1000), "
                "skipping for grid detection (still used via result matrix).",
                template_index, len(filtered),
            )
            continue

        for pt in filtered:
            confidence = float(res[pt[1], pt[0]])
            cell_matches.append((pt[0], pt[1], template_index, confidence))

    if not cell_matches:
        raise ValueError(
            "No cells detected in the screenshot. "
            "Check that the templates match the format. "
        )
    xs = [m[0] for m in cell_matches]
    ys = [m[1] for m in cell_matches]

    rep_w, rep_h = templates[0].shape[::-1]
    cropped_board = img[min(ys):max(ys)+rep_h,min(xs):max(xs)+rep_w]

    logger.info(
        "Board detected: %d total cells, crop size %s",
        len(cell_matches), cropped_board.shape[:2],
    )

    if knn_model_path is not None:
        samples, labels = build_training_data(cell_matches,img_gray, templates)
        if len(samples) > 0:
            all_samples,all_labels = accumulate_training_data(samples,labels,training_data_path)
            knn = train_knn_model(all_samples,all_labels)
            save_knn_model(knn,knn_model_path)
        else:
            logger.warning(
                "No usable training samples produced from cell matches,"
                "skipping KNN save"
            )
    
    return cropped_board, cell_matches, img_gray, match_results