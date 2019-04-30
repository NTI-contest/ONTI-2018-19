# -*- coding: utf-8 -*-
import math
import sys


def find_obj2(pic):
    row_max = len(pic)
    col_max = len(pic[0])
    visited = [[False for j in range(col_max)] for i in range(row_max)]

    colors = {}
    for row in range(row_max - 1, 0, -1):
        for col in range(col_max):
            if not visited[row][col]:
                clr = pic[row][col]
                key = clr + ',' + str(row) + ',' + str(col)
                colors[key] = [(row, col)]
                queue = [(row, col)]
                while len(queue) > 0:
                    r, c = queue.pop(0)  # row, col
                    if not visited[r][c]:
                        visited[r][c] = True
                        colors[key].append((r, c))

                        if r + 1 < row_max:
                            if pic[r + 1][c] == clr and not visited[r + 1][c]:
                                queue.append((r + 1, c))
                        if r - 1 >= 0:
                            if pic[r - 1][c] == clr and not visited[r - 1][c]:
                                queue.append((r - 1, c))
                        if c + 1 < col_max:
                            if pic[r][c + 1] == clr and not visited[r][c + 1]:
                                queue.append((r, c + 1))
                        if c - 1 >= 0:
                            if pic[r][c - 1] == clr and not visited[r][c - 1]:
                                queue.append((r, c - 1))

                if len(colors[key]) < 10:
                    colors.pop(key)
                else:
                    # добавляем площадь цвета от общего размера картинки
                    colors[key].insert(0, len(colors[key]) / (pic_h * pic_w) 
                        * 100)

    # выбираем цвет, у которого минимальная дельта к площади из условий (sq)
    # for clr in colors:
    #    print (clr, len(colors[clr]))

    min_delta = float('inf')
    for key in colors:
        delta = abs(colors[key][0] - sq)
        if  delta < min_delta:
            key_clr = key
            min_delta = delta

    max_x = 0
    for xy in colors[key_clr][1:]:
        if xy[0] > max_x:
            max_x = xy[0]

    return max_x


def avg(arr):
    return sum(arr) / len(arr)

virtual = True

results = []
data = sys.stdin.readlines()

cam_h, cam_alpha, cam_beta, pic_h, pic_w, sq = list(map(int, 
    data[0].strip().split(' ')))
data.pop(0)

"""
cam_h 	        - высота установки камеры, мм
camAlpha 	- угол камеры относительно горизонта, градусы
camBeta		- угол камеры, градусы
picH 	        - высота изображения, пиксели
picW 		- ширина изображения, пиксели
sq  		- минимальная площадь предмета, % от общей площади картинки
"""

picRaw, picDec = [], []

for row in range(pic_h):
    picRaw.append([])
    lineRaw = list(data[row].strip().split(' '))
    picRaw[row] = lineRaw

object_bottom = find_obj2(picRaw) # pixels from picture_bottom to object_bottom
angle = 90 - cam_alpha - cam_beta/2 + (pic_h - object_bottom)/pic_h * cam_beta

result = cam_h * math.tan(math.radians(angle))
print (round(result))
