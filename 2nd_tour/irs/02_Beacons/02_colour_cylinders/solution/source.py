# -*- coding: utf-8 -*-
import sys
import math


def line_len(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def extreme_points(lst):
    max_len = 0
    xy = tuple()
    for i in range(len(lst)):
        x1, y1 = lst[i]
        for j in range(len(lst)):
            if line_len(x1, y1, *lst[j]) > max_len:
                max_len = line_len(x1, y1, *lst[j])
                xy = (x1, y1, *lst[j])
    return xy


data = sys.stdin.readlines()

N, dT = map(int, data[0].strip().split(' '))
"""
N  - кол-во замеров
dT - пауза между замерами, мс
"""
diameter = 20                                           # robots and cylinders, in cm
cylinder_colors = []
cylinder_dist_by_colors = {}

robot_xy = [[0, 0]]
alpha, robot_distance = 0, 0

for i in range(N):
    measures = data[i+1].strip().split(' ')            # v, w, dist_to_cylinder, color
    measures[:3] = list(map(float, measures[:3]))      # v, w, dist_to_cylinder -> float()
    measures[3] = measures[3].rjust(6, '0')
    v, w, dist_to_cyl, color = measures

    alpha += w * dT
    robot_distance = v * dT

    r_x = robot_xy[-1][0] + robot_distance * math.cos(alpha)
    r_y = robot_xy[-1][1] + robot_distance * math.sin(alpha)

    robot_xy.append((r_x, r_y))

    if dist_to_cyl < 255 and color != '000000':
        cyl_x = robot_xy[-1][0] + dist_to_cyl * math.cos(alpha)
        cyl_y = robot_xy[-1][1] + dist_to_cyl * math.sin(alpha)

        if color not in cylinder_dist_by_colors:
            cylinder_dist_by_colors[color] = [(cyl_x, cyl_y)]
        else:
            cylinder_dist_by_colors[color].append((cyl_x, cyl_y))

unique_dist = {}
for key in cylinder_dist_by_colors:
    xy = []
    unique_dist[key] = []
    for x, y in cylinder_dist_by_colors[key]:
        str_xy = str(round(x, 4)) + ',' + str(round(y, 4))
        if str_xy not in xy:
            xy.append(str_xy)
            unique_dist[key].append([x, y])

cylinder_centers = []
for color in unique_dist:
    x1, y1, x2, y2 = extreme_points(cylinder_dist_by_colors[color])
    x3, y3 = cylinder_dist_by_colors[color][8]

    L1 = [(x1 + x2) / 2, (y1 + y2) / 2]
    L2 = [(x2 + x3) / 2, (y2 + y3) / 2]

    # P1
    k1 = (x1 - x2) / (y2 - y1)
    b1 = L1[1] - k1 * L1[0]

    # P2
    k2 = (x2 - x3) / (y3 - y2)
    b2 = L2[1] - k2 * L2[0]

    x = (b1 - b2) / (k2 - k1)
    y = k1 * x + b1

    cylinder_centers.append([x, y, color])

results = []
for i in range(len(cylinder_centers)):
    for j in range(1, len(cylinder_centers)):
                if i != j and i < j:
                    x1, y1 = cylinder_centers[i][0:2]
                    clr1 = cylinder_centers[i][2]
                    x2, y2 = cylinder_centers[j][0:2]
                    clr2 = cylinder_centers[j][2]

                    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                    if dist - diameter < diameter:
                        results.append(sorted([clr1, clr2]))

for i in results:
    print(*i)
