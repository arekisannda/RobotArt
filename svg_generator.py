#!/usr/bin/python

import sys
import os
import random
from math import *
import numpy as np
from argparse import ArgumentParser
import argparse

###############################################################################
PLATE_ANGLE_MIN, PLATE_ANGLE_MAX = 0, 360
ARM1_ANGLE_MIN, ARM1_ANGLE_MAX = -90, 90
ARM2_ANGLE1_MIN, ARM2_ANGLE1_MAX = -90, 90
ARM2_ANGLE2_MIN, ARM2_ANGLE2_MAX = -90, 90

PLATE_INC = 1
ARM1_INC = 1
ARM2_INC1 = 1
ARM2_INC2 = 1

L1 = 160
L2 = 200
L3 = L1 + L2

option_list = ['point', 'points', 'line', 'arc']
save_path = None
c_rad = 10
x_max, y_max = 400, 400
###############################################################################

# returns translation matrix
def translate(s_pnt, d_pnt):
    return (np.subtract(d_pnt, s_pnt))

# returns the rotated point
def rotate(pnt, angle):
    radian = radians(angle)
    rot_m = np.matrix([  [cos(radian), -sin(radian)],
                        [sin(radian), cos(radian)]])
    res_m = np.matmul(rot_m, pnt.T)
    res_m = np.around(res_m, decimals=2)
    return (res_m.T)

def flip_x(pnt):
    return (np.multiply(pnt, [-1, 1]))

def flip_y(pnt):
    return (np.multiply(pnt, [1, -1]))

def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--path', metavar='PATH', type=str, nargs=1, \
            help='File Path')
    parser.add_argument('--option', metavar='TYPE', type=str, nargs=1, \
            help='Type of data generation [point, points, line, arc]')
    parser.add_argument('--count', type=int, nargs='?', \
            help='Number of results to generate. Default: 1000')
    return (parser)

def svgStroke(count):
    x1 = np.matrix([L3, 0])
    arm_1 = np.matrix([L1, 0])
    arm_2 = np.matrix([L2, 0])
    shift_m = np.matrix([L3, L3])
    x2 = np.matrix([0, 0])
            
    stroke_list = []
    i = 0
    while (i < count):
        a1 = random.randint(PLATE_ANGLE_MIN, PLATE_ANGLE_MAX)
        a2 = random.randint(ARM1_ANGLE_MIN, ARM1_ANGLE_MAX)
        a3 = random.randint(ARM2_ANGLE1_MIN, ARM2_ANGLE1_MAX)
        a4 = random.randint(ARM2_ANGLE2_MIN, ARM2_ANGLE2_MAX)

        x1_rot = rotate(x1, a1)

        arm_1_rot = rotate(arm_1, a2)
        arm_1_rot = rotate(arm_1_rot, -a1)
        arm_1_rot = flip_x(arm_1_rot)

        arm_pnt = np.add(x2, x1_rot)
        arm_pnt = np.add(arm_pnt, arm_1_rot)

        arm_2_rot_1 = rotate(arm_2, a3)
        arm_2_rot_1 = rotate(arm_2_rot_1, -a1)
        arm_2_rot_1 = rotate(arm_2_rot_1, a2)
        arm_2_rot_1 = flip_x(arm_2_rot_1)

        arm_2_rot_2 = rotate(arm_2, a4)
        arm_2_rot_2 = rotate(arm_2_rot_2, -a1)
        arm_2_rot_2 = rotate(arm_2_rot_2, a2)
        arm_2_rot_2 = flip_x(arm_2_rot_2)

        mid_ang = (a3 + a4) / 2
        arm_2_rot_3 = rotate(arm_2, mid_ang)
        arm_2_rot_3 = rotate(arm_2_rot_3, -a1)
        arm_2_rot_3 = rotate(arm_2_rot_3, a2)
        arm_2_rot_3 = flip_x(arm_2_rot_3)

        pen_pnt_1 = np.add(x2, x1_rot)
        pen_pnt_1 = np.add(pen_pnt_1, arm_1_rot)
        pen_pnt_2 = np.add(pen_pnt_1, arm_2_rot_2)
        pen_pnt_3 = np.add(pen_pnt_1, arm_2_rot_3)
        pen_pnt_1 = np.add(pen_pnt_1, arm_2_rot_1)

        pen_pnt_1 = np.add(pen_pnt_1, shift_m)
        pen_pnt_2 = np.add(pen_pnt_2, shift_m)
        pen_pnt_3 = np.add(pen_pnt_3, shift_m)
        abs_val = abs(a3 - a4)
        # if (True):
        if  (abs_val >= 15) and (abs_val <= 90) and \
            (abs(pen_pnt_1.item(0) - L3) <= 200) and (abs(pen_pnt_1.item(1) - L3) <= 200) and \
            (abs(pen_pnt_2.item(0) - L3) <= 200) and (abs(pen_pnt_2.item(1) - L3) <= 200) and \
            (abs(pen_pnt_3.item(0) - L3) <= 200) and (abs(pen_pnt_3.item(1) - L3) <= 200):
            stroke_list.append((pen_pnt_1.tolist()[0], pen_pnt_2.tolist()[0], a1, a2, a3, a4))
            i += 1

    header1 =   '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" version="1.1">\n' + \
                '<defs>\n' + \
                '<mine:dataset xmlns:mine="http://example.org/mine">\n'
    header2 =   '</mine:dataset>\n' + \
                '</defs>\n' + \
                '<g transform="translate(-160,560) scale(1,-1)">\n'
    footer='</g></svg>'
    random.shuffle(stroke_list)
    for i in stroke_list:
        pnt1, pnt2, a1, a2, a3, a4 = i
        filename = save_path + "X%.2f_Y%.2f_X%.2f_Y%.2f.svg" % (pnt1[0], pnt1[1], pnt2[0], pnt2[1])
        with open(filename, 'w') as svg_out:
            svg_out.write(header1)
            data =  '<mine:mydata label="pnt1" value="%.2f %.2f" />\n' % (pnt1[0], pnt1[1]) + \
                    '<mine:mydata label="pnt2" value="%.2f %.2f" />\n' % (pnt2[0], pnt2[1]) + \
                    '<mine:mydata label="angles" value="%d %d %d %d" />\n' % (a1, a2, a3, a4)
            svg_out.write(data)
            svg_out.write(header2)
            if (a3 < a4):
                draw_path='<path d="M%.2f %.2f A%d %d 0 0,0 %.2f %.2f" fill="none" stroke="black" stroke-width="5"/>\n' % (pnt1[0], pnt1[1], L2, L2,  pnt2[0], pnt2[1])
            elif (a3 > a4):
                draw_path='<path d="M%.2f %.2f A%d %d 0 0,1 %.2f %.2f" fill="none" stroke="black" stroke-width="5"/>\n' % (pnt1[0], pnt1[1], L2, L2, pnt2[0], pnt2[1])
            svg_out.write(draw_path)
            svg_out.write(footer)

def svgPoint(count):
    header1 =   '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" version="1.1">\n'
    footer='</svg>'
    for i in range(count):
        x = random.randint(c_rad, x_max - c_rad)
        y = random.randint(c_rad, y_max - c_rad) 
        filename = save_path + "X%d_Y%d.svg" % (x, y)
        circle_svg = '<circle cx="%d" cy="%d" r="%d" />' % (x, y, c_rad)
        with open(filename, 'w') as pnt_out:
            pnt_out.write(header1)
            pnt_out.write(circle_svg)
            pnt_out.write(footer)

def svgPoints(count):
    header1 =   '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" version="1.1">\n'
    footer='</svg>'
    for i in range(count):
        x = random.randint(c_rad, x_max - c_rad)
        y = random.randint(c_rad, y_max - c_rad) 
        x1 = random.randint(c_rad, x_max - c_rad)
        y1 = random.randint(c_rad, y_max - c_rad) 
        filename = save_path + "X%d_Y%d_X%d_Y%d.svg" % (x, y, x1, y1)
        circle_svg = '<circle cx="%d" cy="%d" r="%d" />' % (x, y, c_rad)
        circle_svg1 = '<circle cx="%d" cy="%d" r="%d" />' % (x1, y1, c_rad)
        with open(filename, 'w') as pnt_out:
            pnt_out.write(header1)
            pnt_out.write(circle_svg)
            pnt_out.write(circle_svg1)
            pnt_out.write(footer)
def svgLine(count):
    header1 =   '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" version="1.1">\n'
    footer='</svg>'
    for i in range(count):
        x = random.randint(c_rad, x_max - c_rad)
        y = random.randint(c_rad, y_max - c_rad) 
        x1 = random.randint(c_rad, x_max - c_rad)
        y1 = random.randint(c_rad, y_max - c_rad) 
        filename = svg_l_path + "X%d_Y%d_X%d_Y%d.svg" % (x, y, x1, y1)
        line_svg = '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="5" stroke="black"/>' % (x, y, x1, y1)
        with open(filename, 'w') as pnt_out:
            pnt_out.write(header1)
            pnt_out.write(line_svg)
            pnt_out.write(footer)

def main():
    global save_path
    parser = build_parser()
    args = parser.parse_args()
    if (len(sys.argv) > 1) and (args.path) and (args.option):
        save_path = args.path[0] if (len(args.path) > 0) else None
        option_type = args.option[0] if (len(args.option) > 0) else None

        if (not os.path.exists(save_path)):
            os.mkdir(save_path)
        count = args.count if (args.count > 0) else 1000
        if (save_path[-1] != '/'):
            save_path += '/'
        if (option_type) and (save_path):
            if (option_type == 'point'):
                svgPoint(count)
            elif (option_type == 'points'):
                svgPoints(count)
            elif (option_type == 'line'):
                svgLine(count)
            elif (option_type == 'arc'):
                svgStroke(count)
        else:
            parser.print_help()
    else:
        parser.print_help()

    return (0)

if (__name__ == "__main__"):
    main()

