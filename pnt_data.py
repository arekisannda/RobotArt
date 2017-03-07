import numpy as py
import math
import json
import func
from collections import defaultdict

#data values
x_max, x_min, x_inc = 90, -90, 1
y_max, y_min, y_inc = 90, -90, 1
z_max, z_min, z_inc = 720, 0, 1

#joint length
l1 = 160
l2 = 200
l3 = l1 + l2

###############################################################################

joint_ang = []
for i in range(x_min, x_max, x_inc):
    joint_ang.append((i, -i))

all_pnts = []
for i in joint_ang:
    all_pnts.append(func.getPosition(i, l1, l2))

def rotatePnts(pnts, angs):
    rot_pnts = []
    orig = func.getPosition((0, 0), l1, l2)
    for ang_z in range(z_min, z_max, z_inc):
        for i in range(len(all_pnts)):
            r = func.getDist(all_pnts[i], orig)
            res_x, res_y = func.getTransform(all_pnts[i], (l3, 0), ang_z)
            a_res = ((angs[i][0], angs[i][1], ang_z))
            rot_pnts.append(((round(res_x), round(res_y)), a_res))
    return (rot_pnts)

res_pnts = rotatePnts(all_pnts, joint_ang)

d = defaultdict(list)
for i in res_pnts:
    d[i[0]].append(i[1])

def remap(mapping):
     return [{'key':k, 'value': v} for k, v in mapping.items()]

with open('data_pnts.json', 'w') as fp:
    json.dump(remap(d), fp)
