import cv2
import numpy as np
import os
import logging
from screen import deduplicate_points

logger = logging.getLogger(__name__)

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
}

def identify_cells(img,templates, threshold = 0.9):
    """Detects minesweeper cells via template matching
    Returns cropped image and list of classified cells"""
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

        #Skip templates with more than 1000 deduped results
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
    
    return cropped_board, cell_matches, img_gray, match_results