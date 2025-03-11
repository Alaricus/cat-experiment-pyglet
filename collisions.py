def get_collision_direction(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
        overlap_x = min(x1 + w1, x2 + w2) - max(x1, x2)
        overlap_y = min(y1 + h1, y2 + h2) - max(y1, y2)

        if overlap_x > overlap_y:
            if y1 < y2:
                return "NORTH"
            else:
                return "SOUTH"
        else:
            if x1 < x2:
                return "EAST"
            else:
                return "WEST"

    return None
