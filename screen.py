def deduplicate_points(data, condition = None, min_distance = 10):
    #Filter list, keeps points only far enough away from existing
    result = []

    grid = {}
    cell_size = min_distance+1

    for element in data:
        ex,ey = element[0],element[1]
        gx,gy = ex//cell_size, ey//cell_size
        close = False

        for dx in range(-1,2):
            if close:
                break
            for dy in range(-1,2):
                key = (gx+dx,gy+dy)
                if key in grid:
                    for existing in grid[key]:
                        if not (abs(ex-existing[0]) > min_distance or abs(ey-existing[1]) > min_distance):
                            close = True
                            break
        if not close:
            result.append(element)
            grid.setdefault((gx,gy), []).append(element)
    return result

