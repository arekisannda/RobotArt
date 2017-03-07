import math

def getPosition(ang_pair, l1, l2):
    rad_x = math.radians(ang_pair[0])
    rad_y = math.radians(ang_pair[1])
    x_pos = l1 * math.cos(rad_x) + l2 * math.cos(rad_x + rad_y)
    y_pos = l1 * math.sin(rad_x) + l2 * math.sin(rad_x + rad_y)
    return (x_pos, y_pos)

def getDist(p1, p2):
    x_delta = p1[0] - p2[0]
    y_delta = p1[1] - p2[1]

    return (math.sqrt(math.pow(x_delta, 2) + math.pow(y_delta, 2)))

def getTransform(p, c, ang):
    rad = math.radians(ang)

    x_1 = p[0] - c[0]
    y_1 = p[1] - c[1]

    x_2 = (math.cos(rad) * x_1 - math.sin(rad) * y_1) + c[0]
    y_2 = (math.sin(rad) * x_1 + math.cos(rad) * y_1) + c[1]

    return (x_2, y_2)

