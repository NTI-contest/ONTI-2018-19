# -*- coding: utf-8 -*-
import sys
import math
import numpy as np

def cross_find(coords):
    # coords  - массив с координатами 4х угольника (ABCD)
    x1, y1 = coords[0]
    x2, y2 = coords[2]
    x3, y3 = coords[1]
    x4, y4 = coords[3]

    x = -(((x1 * y2 - x2 * y1) * (x4 - x3) - (x3 * y4 - x4 * y3) * (x2 - x1)) / (
                (y1 - y2) * (x4 - x3) - (y3 - y4) * (x2 - x1)))
    y = ((y3 - y4) * (-x) - (x3 * y4 - x4 * y3)) / (x4 - x3)

    return [int(x), int(y)]


def lineToSegments(begin, end, segments = 2):
    # begin, end - массивы с координатами отрезка (начало, конец). начало, как правило - центр
    x0 = round((end[0] - begin[0]) / segments)
    y0 = round((end[1] - begin[1]) / segments)

    points = [begin]
    for i in range(1, segments):
        points.append([])
        points[i].append(points[i - 1][0] + x0)
        points[i].append(points[i - 1][1] + y0)
    points.append([end])
    return points


def rgb2clr(rgb):
    #return (rgb[0] * 256 ** 2 + rgb[1] * 256 + rgb[2])
    if type(rgb) == int:               # один цвет, значит переводим в серый
        rgb = [rgb]
        for i in range(2):
            rgb.append(rgb[0])
    return int(sum([rgb[i] * 256**(2-i) for i in range(len(rgb))]))


def clr2rgb(clr):
    r = (clr & 0xFF0000) >> 16
    g = (clr & 0x00FF00) >> 8
    b = (clr & 0x0000FF)
    return (r, g ,b)


def blur(pic_in): # div, offset):
    blur5 = [
        [0.000789, 0.006581, 0.013347, 0.006581, 0.000789],
        [0.006581, 0.054901, 0.111345, 0.054901, 0.006581],
        [0.013347, 0.111345, 0.225821, 0.111345, 0.013347],
        [0.006581, 0.054901, 0.111345, 0.054901, 0.006581],
        [0.000789, 0.006581, 0.013347, 0.006581, 0.000789]
    ]
    blur3 = [
        [0.054901, 0.111345, 0.054901],
        [0.111345, 0.225821, 0.111345],
        [0.054901, 0.111345, 0.054901]
    ]

    pic_out, pic_blur = [], []
    size = 3                   # "window" size
    side = size //2

    pic_h, pic_w = len(pic_in), len(pic_in[0])
    for i in range(side, pic_h - side):
        pic_out.append([])
        for j in range(side, pic_w - side):

            # pixels - 2D список цветов пикселей "окна" в каналах R,G,B
            # очередное "окно" из пикселей 3*3 для применения фильтра
            pixels = []
            for p_y in range(i-side, i+side+1):
                pixels.append([])
                for p_x in range(j-side, j+side+1):
                    pixels[-1].append(clr2rgb(pic_in[p_y][p_x]))

            # pixels_RGB - 2D список списокв цветов по-канально [R], [G], [B]
            pixels_RGB = []
            for ii in range(3):
                pixels_RGB.append([[rgb[ii] for rgb in row] for row in pixels])

            pic_blur = []
            for channel in range(3):
                pic_blur.append([])
                for ii in range(size):
                    pic_blur[-1].append([])
                    for jj in range(size):
                        if size == 3:
                            pic_blur[-1][-1].append(pixels_RGB[channel][ii][jj] * blur3[ii][jj])
                        elif size == 5:
                            pic_blur[-1][-1].append(pixels_RGB[channel][ii][jj] * blur5[ii][jj])

            pixels_RGB_blur = [int(sum([sum(row) for row in ch_blur])) for ch_blur in pic_blur]
            pic_out[-1].append(rgb2clr(pixels_RGB_blur))

    return pic_out


def pic_to_RGB (pic_in):
    pic_out = []
    for row in range(len(pic_in)):
        pic_out.append([])
        for col in range(len(pic_in[0])):
            pic_out[-1].append(clr2rgb(pic_in[row][col]))
    return pic_out


def rgb2grey(pic_in, mode):
    RGB, pic_out = [], []
    pic_h, pic_w = len(pic_in), len(pic_in[0])
    for i in range(pic_h):
        pic_out.append([])
        for j in range(pic_w):
            RGB = clr2rgb(pic_in[i][j])
            if mode == 1:               # "V from HSV", V = max(r, g, b)
                result = max(RGB)
            elif mode == 2:            # через Y ' from Y'UV(средневзвешенное) вариант 1
                # result = Math.round((0.299 * RGB[0]) + (0.587 * RGB[1]) + (0.114 * RGB[2]))
                result = round((0.2126 * RGB[0]) + (0.7152 * RGB[1]) + (0.0722 * RGB[2]))
            elif mode == 3:  # через Y ' from Y' UV(средневзвешенное) вариант 2
                clr = pic_in[i][j]
                # tmp = ((((clr >> 16) & 0xff) * 76) + (((clr >> 8) & 0xff) * 150) + ((clr & 0xff) * 29)) >> 8
                tmp = ((((clr >> 16) & 0xff) * 76) + (((clr >> 8) & 0xff) * 150) + ((clr & 0xff) * 29)) >> 8
                result = tmp << 16 | tmp << 8 | tmp  # r | g | b
            elif mode == 4:         # Поиск ближайшей точки нейтральной оси: L = (max(R, G, B) + min(R, G, B)) / 2
                result = round((max(RGB) + min(RGB)) / 2)
            elif mode == 5:         # Среднее арифметическое компонент R, G, B
                result = round(sum(RGB) / 3)

            #print (result,rgb2clr(result))
            pic_out[-1].append(rgb2clr(result))

    return pic_out


def rgb2bw(pic_in, method = 'niblack'):
    #pic_in_RGB = pic_to_RGB(pic_in)

    pic_h, pic_w = len(pic_in), len(pic_in[0])
    pic_out = [[16777215 for _ in range(pic_w)] for _ in range(pic_h)]

    delta = 0
    dot_side = 3
    radius = int(dot_side/2)                    # pixels from center 'big dot' to each side

    if method == 'niblack' or method == 'sauvola':
        '''
        Niblack:
        T = m + k * s
        m - mean of local area pixels
        k - 0.2     - value by author
        s - standart deviation of local pixel area

        Sauvola:
        T = m * (1 - k * 1 - S / R)
        m - mean of pixels under window area
        S - dynamic range of variance
        k - may be in the range of 0-1 (?)
        k=0.5 and R=128         - values by author

        '''
        for row in range(delta + radius, pic_h - delta - radius):
            for col in range(delta + radius, pic_w - delta - radius):
                pixels = []
                for p_r in range(dot_side):
                    for p_c in range(dot_side):
                        pixels.append(pic_in[row - radius + p_r][col - radius + p_c])
                #print (row,col,list(map(hex, pixels)))
                mean = sum(pixels)/len(pixels)
                if method == 'niblack':
                    sd = standart_deviation(pixels)
                    T = int(mean + sd * 0.2)
                    #print (mean, T)
                else:
                    S = standart_variance(pixels)
                    T = int(mean * (1 - 0.5 * (1 - S / 128)))

                # pix = 16777215 if pic_in[row][col] >= T else 0
                if pic_in[row][col] < T:
                    pic_out[row][col] = 0

    elif method == 'threshold':
        for row in range(pic_h):
            for col in range(pic_w):
                if pic_in[row][col] < 1500000:
                    pic_out[row][col] = 1
                else:
                    pic_out[row][col] = 0

    return pic_out


def standart_deviation(nums):
    mean = sum(nums)/len(nums)
    return ((1/len(nums) * sum([(num - mean) **2 for num in nums])/(len(nums))) ** 0.5)


def standart_variance(nums):
    mean = sum(nums)/len(nums)
    return (sum([(num - mean) **2 for num in nums])/len(nums))


def k_b(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    k = (y2 - y1) / (x2 - x1)
    b = y2 - k * x2
    return (k, b)

def mean_xy(corner1, corner2):
    # вычисление средних координат x, y двух точек
    mean_x = int(corner1[0] + corner2[0]) / 2
    mean_y = int(corner1[1] + corner2[1]) / 2
    return (mean_x, mean_y)


def bias_xy(corner, m_xy):
    # отклонение координат x, y  от среднего значения
    return (abs(corner[0] - m_xy[0]), abs(corner[1] - m_xy[1]))


def close_corners(corners):
    BIAS = 10                               # допустимая погрешность
    abcd = [()] * 4

    meanXY = mean_xy(corners[0],corners[1])
    bias = bias_xy(corners[0], meanXY)
    print (corners[6], corners[0])
    if sum(bias) > BIAS and (corners[6] != corners[0] and corners[2] != corners[1]):
        k1, b1 = k_b(corners[6], corners[0])
        k2, b2 = k_b(corners[2], corners[1])
        x = (b1 - b2) / (k2 - k1)
        y = k1 * x + b1
    else:
        x, y = meanXY
    abcd[0] = (int(x), int(y))

    meanXY = mean_xy(corners[2], corners[3])
    bias = bias_xy(corners[3], meanXY)
    if sum(bias) > BIAS and (corners[1] != corners[2] and corners[5] != corners[3]):
        k1, b1 = k_b(corners[1], corners[2])
        k2, b2 = k_b(corners[5], corners[3])
        x = (b1 - b2) / (k2 - k1)
        y = k1 * x + b1
    else:
        x, y = meanXY
    abcd[1] = (int(x), int(y))

    meanXY = mean_xy(corners[4], corners[5])
    bias = bias_xy(corners[4], meanXY)
    if sum(bias) > BIAS and (corners[3] != corners[5] and corners[7] != corners[4]):
        k1, b1 = k_b(corners[3], corners[5])
        k2, b2 = k_b(corners[7], corners[4])
        x = (b1 - b2) / (k2 - k1)
        y = k1 * x + b1
    else:
        x, y = meanXY
    abcd[2] = (int(x), int(y))

    meanXY = mean_xy(corners[7], corners[6])
    bias = bias_xy(corners[7], meanXY)
    if sum(bias) > BIAS and (corners[4] != corners[7] and corners[0] != corners[6]):
        k1, b1 = k_b(corners[4], corners[7])
        k2, b2 = k_b(corners[0], corners[6])
        x = (b1 - b2) / (k2 - k1)
        y = k1 * x + b1
    else:
        x, y = meanXY
    abcd[3] = (int(x), int(y))

    return abcd


def get_corners(pic_in):
    corners = [(-1, -1)] * 8       # left_up x 2, right_up x2, right_down x2, left_down x2
    #pic_h, pic_w = len(pic_in), len(pic_in[0])

    out_l = out_r = False
    for row in range(pic_h):                        # Up -> Down
        for col_l in range(pic_w):                  # L -> R
            if pic_in[row][col_l] == 1 and not out_l:
                corners[0] = (row, col_l)
                out_l = True

        for col_r in range(pic_w-1, -1, -1):        # L <- R
            if pic_in[row][col_r] == 1 and not out_r:
                corners[1] = (row, col_r)
                out_r = True

    out_l = out_r = False
    for row in range(pic_h-1, -1, -1):              # Up <- Down
        for col_l in range(pic_w):                  # L -> R
            if pic_in[row][col_l] == 1 and not out_l:
                corners[4] = (row, col_l)
                out_l = True

        for col_r in range(pic_w-1, -1, -1):        # L <- R
            if pic_in[row][col_r] == 1 and not out_r:
                corners[5] = (row, col_r)
                out_r = True

    out_u = out_d = False
    for col in range(pic_w):                        # Left -> Right
        for row_u in range(pic_h):                  # U -> D
            if pic_in[row_u][col] == 1 and not out_u:
                corners[6] = (row_u, col)
                out_u = True

        for row_d in range(pic_h-1, -1, -1):        # D <- U
            if pic_in[row_d][col] == 1 and not out_d:
                corners[7] = (row_d, col)
                out_d = True

    out_u = out_d = False
    for col in range(pic_w-1, -1, -1):              # Left <- Right
        for row_u in range(pic_h):                  # U -> D
            if pic_in[row_u][col] == 1 and not out_u:
                corners[2] = (row_u, col)
                out_u = True

        for row_d in range(pic_h-1, -1, -1):        # D <- U
            if pic_in[row_d][col] == 1 and not out_d:
                corners[3] = (row_d, col)
                out_d = True

    print(corners)
    if sum(map(len, corners)) == 0:                             # не найдено ни одного угла
        return -1
    elif no_corner(corners[0], corners[1]) or no_corner(corners[2], corners[3]) or \
        no_corner(corners[4], corners[5]) or no_corner(corners[6], corners[7]):
        return -1                                              # нету одного из углов
    else:
        return close_corners(corners)


def find_corners2(pic_in, delta = 0):

    looked = []

    def check_xy(yx):
        if pic_h - delta > yx[0] >= 0 + delta and pic_w - delta > yx[1] >= 0 + delta:
            return yx not in looked and pic_in[yx[0]][yx[1]] == 1
        else:
            return False


    def find_x(y0x0, direction = 1):
        print (y0x0)
        y0, x0 = y0x0
        prev_yx = (0, 0)
        dX, dY = prev_yx

        while True:
            y, x = y0, x0
            if check_xy((y - direction, x)):
                y -= direction
                dY += 1
            elif check_xy((y, x + direction)):
                x += direction
                dX += 1
            elif check_xy((y + direction,x)):
                y += direction
                dY += 1

            if (y, x) not in perimeter:
                perimeter.append((y, x))

            if x != x0 and dY > 0:
                dX, dY = 0, 0

            if x == x0 and dY > 1:
                looked.pop()
                return (prev_yx)

            #print('yx0:',y0, x0, '   yx:', y, x, '   ', y0 == y, x0 == x, '  dYX:',dY, dX)
            looked.append((y, x))
            prev_yx = (y0, x0)
            if y0 == y and x0 == x:
                x += direction
            y0, x0 = y, x


    def find_y(y0x0, direction = 1):
        y0, x0 = y0x0
        prev_yx = (0, 0)
        dX, dY = prev_yx

        while True:  # from up to down
            y, x = y0, x0
            if check_xy((y, x + direction)):
                x += direction
                dX += 1
            elif check_xy((y + direction, x)):
                y += direction
                dY += 1
            elif check_xy((y, x - direction)):
                x -= direction
                dX += 1

            if (y, x) not in perimeter:
                perimeter.append((y, x))

            if y0 != y and dX > 0:
                dX, dY = 0, 0

            if y == y0 and dX > 1:
                looked.pop()
                return prev_yx

            #print('yx0:',y0, x0, '   yx:', y, x, '   ', y0 == y, x0 == x, '  dYX:',dY, dX, '  black[y,x]:',pic_in[y][x],' look:', (y,x) in looked)

            looked.append((y, x))
            prev_yx = (y0, x0)
            if y0 == y and x0 == x:
                if (y,x) not in looked:
                    y += direction
                else:
                    break
            y0, x0 = y, x

    pic_h, pic_w = len(pic_in), len(pic_in[0])
    start = (-1, -1)

    for y in range(delta, pic_h - delta):
        for x in range(delta, y + 1): # (delta):
            if pic_in[x][y - x + delta] == 1:
                start = (x, y - x + delta)
                break
        if sum(start) >= 0:
            break

    perimeter = [start]
    corners0 = [start]
    corners0.append(find_x(corners0[-1]))
    corners0.append(find_y(corners0[-1]))
    print (corners0)
    corners0.append(find_x(corners0[-1], -1))
    find_y(corners0[-1], -1)                     # для заполнения точек периметра

#    for i in perimeter:
#        print (*i)

    corners = corners0.copy()

    def corner_at_border(xy):
        return xy[0] == pic_h-1 or xy[0] == 0 or xy[1] == pic_w - 1 or xy[1] == 0

    if not corner_at_border(corners[0]) or not corner_at_border(corners[1]) or \
        not corner_at_border(corners[2]) or not corner_at_border(corners[3]):
        c = 1
        for (y0, x0) in corners0:
            dX = sum([1 for y, x in perimeter if y == y0]) - 1
            dY = sum([1 for y, x in perimeter if x == x0]) - 1
            yx = (y0, x0)

            if dY > dX:
                if (y0 + dY, x0) in perimeter:
                    yx = (y0 + dY, x0)
                else:
                    yx = (y0 - dY, x0)
            elif dX > dY:
                if (y0, x0 + dX) in perimeter:
                    yx = (y0, x0 + dX)
                else:
                    yx = (y0, x0 - dX)
            corners.insert(c, yx)
            c += 2

        #for c in corners:
        #    print (*c)

    return corners


def no_corner(c1, c2):
    if sum(c1) < 0 or sum(c2) < 0:
        return True


def decode_artag(abcd):
    center = cross_find(abcd)              # center of ARTag
    parity = pic_bw[center[0]][center[1]]

    '''
       K (keys) cells
       -------------
       | 3 |   | 0 |
       -------------
       |   |   |   |
       -------------
       | 2 |   | 1 |
       -------------
    '''
    # отрезки от центр к углам
    # из полученных точек берем только [1], т.к. [0] - это центр метки
    K = []
    for i in range(4):
        K.append(tuple(map(int, lineToSegments(center, abcd[i], 3)[1])))
    #print('K',K)

    KEY = -1
    for i in range(4):
        y, x = K[i]
        if pic_bw[y][x] == 0:
            KEY = i
            break
    print ('key',KEY)
    if KEY == -1:                                   # не найдена "ключевая" клетка
        return -1

    '''
       bin's cells
       -------------
       |   | 3 |   |
       -------------
       | 2 |   | 0 |
       -------------
       |   | 1 |   |
       -------------
    '''

    bins = []
    for i in range(4):
        x, y = map(int, lineToSegments(K[i], K[(i+1) % 4])[1])
        bins.append(pic_bw[x][y])
    print ('bins', bins)
    states = [(2, 3, 1, 0), (3, 2, 0, 1), (0, 3, 1, 2), (1, 0, 2, 3)]

    bin_num = ''
    for i in range(4):
        bin_num += str(bins[states[KEY][i]])

    # четное "1" - бит Ч в "0",    нечетое "1" - бит Ч в "1"
    if bin_num.count('1') % 2 == 0 and parity == 0 or \
            bin_num.count('1') % 2 != 0 and parity == 1:                # проверка на бит четности
        return int(bin_num, 2)
    else:
        return -1                                                       # не прошел контроль четности


def bfs_edges(pic_in):
    def check_range(y, x):
        if pic_h > y >= 0 and pic_w > x >= 0:
            return True
        else:
            return False

    def check_white(y, x):
        for i in range(3):
            for j in range(3):
                if i == j == 1:
                    break
                if check_range(y - 1 + i, x - 1 + j):
                    if pic_in[y - 1 + i][x - 1 + j] == 0:           # white pixel
                        return True
        return False

    def check_black(y, x):
        bl = 0
        for i in range(3):
            for j in range(3):
                if check_range(y - 1 + i, x - 1 + j):
                    if pic_in[y - 1 + i][x - 1 + j] == 1:           # black pixel
                        bl += 1
        if bl < 7:
            return True
        else:
            return False

    pic_h, pic_w = len(pic_in), len(pic_in[0])
    start = (-1, -1)
    for i in range(pic_h):
        for j in range(i):
            if pic_in[j][i-j] == 1:
                start = (j, i-j)
                break
        if sum(start) >= 0:
            break

    visited = [[False for _ in range(pic_w)] for _ in range(pic_h)]
    queue = [start]
    edges = []
    while len(queue) > 0:
        y, x = queue.pop(0)
        if not visited[y][x]:
            visited[y][x] = True
            if check_white(y, x):
                edges.append((y, x))
            elif (x == 0 or y == 0) and check_black(y, x):
                edges.append((y, x))
            elif (x == pic_w-1 or y == pic_h-1) and check_black(y, x):
                edges.append((y, x))

            for i in range(3):
                for j in range(3):
                    if not i == j == 1:
                        yy = y - 1 + i
                        xx = x - 1 + j
                        if check_range(yy, xx) and not visited[yy][xx] and pic_in[yy][xx] == 1:     # black pixel
                            queue.append((yy, xx))

        if (y, x) == start and len(edges) > 1:
            break

    # оставляем только периметр из точек
    perimeter = []
    looked = []
    queue = [edges[0]]
    while len(queue) > 0:
        y0, x0 = queue.pop(0)
        if not (y0, x0) in looked:
            looked.append((y0, x0))
            perimeter.append((y0, x0))
            for y, x in edges:
                dY = abs(max(y0, y) - min(y0, y))
                dX = abs(max(x0, x) - min(x0, x))
                if (dY <= 1 and dX <= 1) and (y, x) not in looked and (y, x) not in queue:
                    queue.append((y, x))

    return perimeter


path = "C:\\_docs\\!RobonesT\\!!Проекты\\Разбор НТИ ИРС\\zad7\\"
fileIn = path + "datasets\\0"
fileOut = path + "zad7_out.txt"

with open(fileIn) as f:
    data = f.readlines()

# data = sys.stdin.readlines()
shots_n, pic_h, pic_w = list(map(int, data[0].strip().split(' ')))
data.pop(0)
"""
#shots_h    - кол-во замеров камерой
#pic_h	    - ширина изображения, пиксели
#pic_w	    - высота изображения, пиксели
"""

pics_dec = []
for picN in range(shots_n):
    pics_dec.append([])
    for row in range(pic_h):
        line = list(map(lambda h: int(h, 16), data[row + picN * pic_h].strip().split(' ')))
        pics_dec[picN].append(line)

print ('get file done')

pic_grey = rgb2grey(pics_dec[0], 2)
hist = {}
for row in pic_grey:
    for clr in row:
        clr_rgb0 = clr2rgb(clr)[0]
        if str(clr_rgb0) not in hist:
            clr_txt = str(clr_rgb0).rjust(3,'0')
            hist[clr_txt] = 1
        else:
            hist[clr_txt] += 1

for k, v in hist.items():
    print(k, v)

pic_blur = blur(pic_grey)

pic_bw = rgb2bw(pic_blur, 'threshold')

with open(fileOut, mode='w') as f:
    for line in pic_bw:
        f.write(','.join(list(map(str,line))) + '\n')

print(find_corners2(pic_bw, 5))

#z = np.array(pic_bw, dtype = int)

#for i in z:
#print (sum(z[:,41]))
#ed = bfs_edges(pic_bw)
#print (ed)
#corners = [(-1,-1)] * 8
#print (sorted(ed))
#corners[0] = ed[0]
#for y in ed:
#    print (*y)


"""

results = []
for i in range(shots_n):
    pic_bw = rgb2bw(pics_dec[i],'threshold')
    cs = get_corners(pic_bw)
    if cs == -1:
        res = -1
    else:
        res = decode_artag(cs)
    results.append(res)
    print ('result', results)

# vertical output
'''
spc = '16711680,' * pic_w						# красный цвет
spc = spc[:-1] + '\n'
with open(fileOut, mode='w') as f:
for i in pics_dec[0]:
    #for j in range(len(pics_dec[0])):
       #f.write(','.join(list(map(str, pics_dec[i][j]))) + '\n')
   f.write(str(i).replace("[","").replace("]","") + '\n')
f.write(spc)
f.write(spc)
'''

# horizontal output
'''
spc = '16711680, 16711680, 16711680'
pics_out = []
for i in range(pic_h):
    line = ''
    for shot in range(shots_n):
        line += ','.join(list(map(str, pics_dec[shot][i])))
        line += ' ,' + spc
    pics_out.append(line)
'''

"""

#with open(fileOut, mode='w') as f:
 #   for line in pic_bw:
 #       f.write(','.join(list(map(str,line))) + '\n')


