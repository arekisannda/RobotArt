from xml.dom import minidom
import re
import sys
import fileinput

###############################################################################
x_offset = -230
y_offset = -230
###############################################################################

if (len(sys.argv) != 3):
    print ("Usage python parse_svg.py <filename> <output file>")
    exit()

doc = minidom.parse(sys.argv[1])
path_list = doc.getElementsByTagName('path')
rect_list = doc.getElementsByTagName('rect')
line_list = doc.getElementsByTagName('line')
poll_list = doc.getElementsByTagName('polyline')
polg_list = doc.getElementsByTagName('polygon')

element_list = []

for rect in rect_list:
    print ("rectangle")
    rect_x = rect.getAttribute('x')
    rect_y = rect.getAttribute('y')
    rect_w = rect.getAttribute('width')
    rect_h = rect.getAttribute('height')

    if (not rect_x) or (not rect_y) or (not rect_w) or (not rect_h):
        print ("Invalid Rect Element")
    else:
        rect_x = int(float(rect_x)) + x_offset
        rect_y = int(float(rect_y)) + y_offset
        rect_w = int(float(rect_w))
        rect_h = int(float(rect_h))
        pt_0 = (rect_x, rect_y)
        pt_1 = (rect_x + rect_w, rect_y)
        pt_2 = (rect_x + rect_w, rect_y + rect_h)
        pt_3 = (rect_x, rect_y + rect_h)

        rect_path = [pt_0, pt_1, pt_2, pt_3, pt_0]
        element_list.append(rect_path)

for line in line_list:
    print ("line")
    x_1 = line.getAttribute('x1')
    y_1 = line.getAttribute('y1')
    x_2 = line.getAttribute('x2')
    y_2 = line.getAttribute('y2')

    if (not x_1) or (not y_1) or (not x_2) or (not y_2):
        print ("Invalid Line Element")
    else:
        x_1 = int(float(x_1)) + x_offset
        y_1 = int(float(y_1)) + y_offset
        x_2 = int(float(x_2)) + x_offset
        y_2 = int(float(y_2)) + y_offset
        pt_0 = (x_1, y_1)
        pt_1 = (x_2, y_2)
        line_path = [pt_0, pt_1]
        element_list.append(line_path)

for poll in poll_list:
    print ("polyline")
    points = poll.getAttribute('points')
    
    if (not points):
        print ("Invalid Polyline")
    else:
        poll_path = [(int(float(crd[0])) + x_offset, int(float(crd[1])) + y_offset)\
                for crd in (pts.split(",") for pts in points.split())]
        element_list.append(poll_path)

for polg in polg_list:
    print ("polygon")
    points = polg.getAttribute('points')
    
    if (not points):
        print ("Invalid Polygon")
    else:
        polg_path = [(int(float(crd[0])) + x_offset, int(float(crd[1])) + y_offset)\
                for crd in (pts.split(",") for pts in points.split())]
        element_list.append(polg_path)

def getXY(nums):
    val = re.search("(-?[0-9]*(\.[0-9][0-9]*)?)", nums)
    x_val = val.group(0)
    nums = nums[len(x_val):].lstrip()
    val = re.search("(-?[0-9]*(\.[0-9][0-9]*)?)", nums)
    y_val = val.group(0)
    nums = nums[len(y_val):].lstrip()
    return (x_val, y_val, nums)


for path in path_list:
    path_string = path.getAttribute('d')
    
    split_letters = re.findall('[A-Z|a-z][^A-Z|a-z]*', path_string)
    path_elements = []
    for chunk in split_letters:
        char = chunk[0]
        nums = chunk[1:].replace(',', ' ').lstrip().rstrip()
    
        if (char == 'm') or (char == 'M'):
            if (path_elements):
                element_list.append(path_elements)
                path_elements = []
            while (nums):
                x_val, y_val, nums = getXY(nums)
                if (not x_val) or (not y_val):
                    print ("Invalid Path")
                    break
                else:
                    x_val = int(float(x_val))
                    y_val = int(float(y_val))
                    if (not path_elements):
                        x_val = x_val + x_offset
                        y_val = y_val + y_offset
                    if (char == 'm') and (path_elements):
                        x_val = x_val + path_elements[-1][0]
                        y_val = y_val + path_elements[-1][1]
                    path_elements.append((x_val, y_val))
        elif (char == 'l') or (char == 'L'):
            while (nums):
                x_val, y_val, nums = getXY(nums)
                if (not x_val) or (not y_val):
                    print ("Invalid Path")
                    break
                else:
                    x_val = int(float(x_val))
                    y_val = int(float(y_val))
                    if (not path_elements):
                        x_val = x_val + x_offset
                        y_val = y_val + y_offset
                    if (char == 'l') and (path_elements):
                        x_val = x_val + path_elements[-1][0]
                        y_val = y_val + path_elements[-1][1]
                    path_elements.append((x_val, y_val))
        elif (char == 'h') or (char == 'H'):
            val = re.search("(-?[0-9]*(\.[0-9][0-9]*)?)", nums)
            x_val = val.group(0)
            nums = nums[len(x_val):].lstrip()
            y_val = 0
            if (not x_val):
                print ("Invalid Path")
            else:
                x_val = int(float(x_val))
                y_val = y_val
                if (not path_elements):
                    x_val = x_val + x_offset
                    y_val = y_val + y_offset
                if (path_elements):
                    if (char == 'h'):
                        x_val = x_val + path_elements[-1][0]
                    y_val = path_elements[-1][1] + y_offset
                path_elements.append((x_val, y_val))
        elif (char == 'v') or (char == 'V'):
            val = re.search("(-?[0-9]*(\.[0-9][0-9]*)?)", nums)
            y_val = val.group(0)
            nums = nums[len(y_val):].lstrip()
            x_val = 0
            if (not y_val):
                print ("Invalid Path")
            else:
                x_val = x_val
                y_val = int(float(y_val))
                if (not path_elements):
                    x_val = x_val + x_offset
                    y_val = y_val + y_offset
                if (path_elements):
                    if (char == 'v'):
                        y_val = y_val + path_elements[-1][1]
                    x_val = path_elements[-1][0] + x_offset
                path_elements.append((x_val, y_val))
        elif (char == 'z') or (char == 'Z'):
            if (path_elements):
                path_elements.append(path_elements[0])
                element_list.append(path_elements)
                path_elements = []
            else:
                print ("Invalid Path")
    if (path_elements):
        element_list.append(path_elements)
doc.unlink()

with open(sys.argv[2], 'w') as outf:
    for element in element_list:
        outf.write("G0 X%d Y%d P0\n" % (element[0]))
        element = element[1:]
        for crd in element:
            outf.write("G1 X%d Y%d P1\n" % (crd))
