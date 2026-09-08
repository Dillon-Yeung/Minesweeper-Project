import numpy as np
import cv2
import os
import logging
from scanner_local import identify_cells, TEMPLATE_LABEL_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

np.set_printoptions(linewidth=100)

def load_templates(compare_dir):
    template_specs = [
        ("cover.png", "covered"),
        ("empty.png", "empty"),
        ("1.png", "one"),
        ("2.png", "two"),
        ("3.png", "three"),
        ("4.png", "four"),
        ("5.png", "five"),
        ("6.png", "six"),
        ("7.png", "seven"),
        ("8.png", "eight"),
    ]
    templates = []
    for filename, description in template_specs:
        path = os.path.join(compare_dir, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        assert img is not None, f"Template '{filename}' ({description}) not found at {path}"
        templates.append(img)
    return tuple(templates)

def scan_board(test_case, rows, cols, templates):
    _, cell_matches, img_gray, _ = identify_cells(test_case,templates)
    if not cell_matches:
        raise ValueError("No cells detected")

    expected_cells = rows*cols

    from collections import Counter

    tmpl_counts = Counter(m[2] for m in cell_matches)
    max_for_grid = max(expected_cells *2,10)
    grid_matches = [m for m in cell_matches if tmpl_counts[m[2]] <= max_for_grid]

    if not grid_matches:
        grid_matches = cell_matches

    all_xs = sorted(set(m[0] for m in grid_matches))
    all_ys = sorted(set(m[1] for m in grid_matches))

    row_positions = _cluster_positions(all_ys)
    col_positions = _cluster_positions(all_xs)
    

    cell_h,cell_w = templates[0].shape

    row_positions = _extrapolate_positions(row_positions, rows, cell_h)
    col_positions = _extrapolate_positions(col_positions, cols, cell_w)

    logger.info(
        "Grid positions: %d rows x %d cols (from %d matches)",
        len(row_positions), len(col_positions), len(cell_matches),
    )

    max_tmpl_h = max(t.shape[0] for t in templates)
    max_tmpl_w = max(t.shape[1] for t in templates)

    board = np.full((rows,cols),-99, dtype=int)

    for row_idx in range(min(rows,len(row_positions))):
        for col_idx in range(min(cols, len(col_positions))):
            pixel_y = row_positions[row_idx]
            pixel_x = col_positions[col_idx]
            cell_region = img_gray[pixel_y:pixel_y+max_tmpl_h,
                                   pixel_x:pixel_x+max_tmpl_w]

            if cell_region.shape[0] == 0 or cell_region.shape[1] == 0:
                board[row_idx,col_idx] = -1
                continue

            pad_h = max_tmpl_h - cell_region.shape[0]
            pad_w = max_tmpl_w - cell_region.shape[1]

            if pad_h > 0 or pad_w > 0:
                cell_region = np.pad(cell_region, ((0,pad_h),(0,pad_w)),mode='edge')

            best_score = np.inf
            best_template_index = 1

            for tmpl_idx, tmpl in enumerate(templates, start=1):
                th, tw = tmpl.shape
                if cell_region.shape[0] < th or cell_region.shape[1] < tw:
                    continue
                res = cv2.matchTemplate(cell_region,tmpl,cv2.TM_SQDIFF_NORMED)
                score = float(res.min())
                if score < best_score:
                    best_score = score
                    best_template_index = tmpl_idx
            board_value = TEMPLATE_LABEL_MAP.get(best_template_index, best_template_index)
            board[row_idx,col_idx] = board_value

            if best_score > 0.3:
                logger.debug("Low-confidence match at (%d, %d): template %d"
                             "(value = %d) score=%.3f",
                             row_idx, col_idx, best_template_index,
                             board_value, best_score,)
    unmatched = np.count_nonzero(board == -99)

    if unmatched > 0:
        logger.warning(
                "%d cells could not be classified, defaulting to -1 (covered).",
                unmatched,
            )
        board[board == -99 ] = -1
    return board

def _cluster_positions(sorted_values, tolerance=15):
    if not sorted_values:
        return []

    clusters = [[sorted_values[0]]]
    for val in sorted_values[1:]:
        if val-clusters[-1][-1] <= tolerance:
            clusters[-1].append(val)
        else:
            clusters.append([val])

    return [int(np.mean(c)) for c in clusters]

def _extrapolate_positions(detected, expected_count, cell_size):
    if len(detected) >= expected_count:
        return detected[:expected_count]

    if not detected:
        return [i * cell_size for i in range(expected_count)]

    if len(detected) >= 2:
        gaps = [detected[i+1] - detected[i] for i in range(len(detected) -1)]
        step = int(np.mean(gaps))
    else:
        step = cell_size

    positions = list(detected)
    while len(positions) < expected_count:
        positions.append(positions[-1] + step)

    return positions

def _find_nearest_index(positions, value):
    distances = [abs(p-value) for p in positions]
    return distances.index(min(distances))

if __name__ == "__main__":
    import traceback as _tb
    _base = os.path.dirname(os.path.abspath(__file__))
    _results_path = os.path.join(_base, 'board_results.txt')

    try:
        compare_dir = os.path.join(_base, 'compare')
        screenshots_dir = os.path.join(_base, 'screenshots')
        templates = load_templates(compare_dir)

        results = []

        test_img_small = cv2.imread(os.path.join(screenshots_dir, 'screenshot-23.png'))
        if test_img_small is not None:
            logger.info("=== Test: 2x2 board (screenshot-23) ===")
            board_small = scan_board(test_img_small, 2, 2, templates)
            results.append("2x2 Board:")
            results.append(str(board_small))
        else:
            results.append("screenshot-23.png not found")

        test_img_full = cv2.imread(os.path.join(screenshots_dir, 'screenshot-22.png'))
        if test_img_full is not None:
            logger.info("=== Test: 16x30 board (screenshot-22) ===")
            board_full = scan_board(test_img_full, 16, 30, templates)
            results.append("\n16x30 Board:")
            results.append(str(board_full))
        else:
            results.append("screenshot-22.png not found")

        test_img_med = cv2.imread(os.path.join(screenshots_dir, 'screenshot-4.png'))
        if test_img_med is not None:
            logger.info("=== Test: 16x16 board (screenshot-4) ===")
            board_med = scan_board(test_img_med, 16, 16, templates)
            results.append("16x16 Board:")
            results.append(str(board_med))
        else:
            results.append("screenshot-4.png not found")
        with open(_results_path, 'w') as f:
            f.write('\n'.join(results))

    except Exception:
        with open(_results_path, 'w') as f:
            f.write("ERROR:\n")
            _tb.print_exc(file=f)