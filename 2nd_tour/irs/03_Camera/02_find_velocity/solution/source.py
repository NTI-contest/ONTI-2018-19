# -*- coding: utf-8 -*-

import math
import sys

def check(mat1, mat2):  #функция для нахождения смещения между двумя кадрами
    maximum = 0
    max_y = 0
    max_x = 0
    for i in range(-pic_h + 1, pic_h):
        for j in range(-pic_w + 1, pic_w):
            max_this = 0
            for y in range(pic_h):
                for x in range(pic_w):
                    if (y + i) >= 0 and (x + j) >= 0 and (y + i) < pic_h and 
                       (x + j) < pic_w:
                        if mat1[y][x] == mat2[y + i][x + j]:
                            max_this += 1
            if max_this > maximum:
                max_x = -j
                max_y = -i
                maximum = max_this
    return [maximum, max_x, max_y]

data = sys.stdin.readlines()

shots_n, cam_h, cam_alpha, pic_h, pic_w = list(map(int, data[0].strip().split(' ')))
data.pop(0)
'''
#shots_n    - кол-во замеров
#h  	    - высота установки камеры, мм
#cam_alpha  - угол обзора камеры, градусы
#pic_h	    - высота изображения
#pic_w	    - ширина изображения
'''
shots = []

for i in range(shots_n):
    shots.append([]) # очередной кадр
    shot_raw = data[i].strip().split(' ') 
    # кадр в виде одномерного массива пикселей в hex
    shot_dec = list(map(lambda hx: int(hx,16), shot_raw)) 
    # кадр в виде одномерного массива пикселей в dec
    for r in range(0, pic_h * pic_w, pic_w):
        shots[-1].append(shot_dec[r:r + pic_w]) 
        # очередная строка пикселей в кадре i

x, y = 0, 0
for i in range(1, shots_n):
    temp = check(shots[i-1], shots[i])

    x += int(temp[1])
    y += int(temp[2])

x = math.tan(math.radians(cam_alpha / 2)) * 2 * cam_h / pic_w * x
y = math.tan(math.radians(cam_alpha / 2)) * 2 * cam_h / pic_h * y
print(str(round(x, 1)) + " " + str(round(y, 1)))
