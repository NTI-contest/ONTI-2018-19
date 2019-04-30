import cv2 as cv
import numpy as np
from engines import *

# Подключение камеры
cap = cv.VideoCapture(0)
pi, ESC, STEER = setup_gpio()
if cap.isOpened() == False:
    print("cannot open port")
    exit()
img_size = [360, 200]

# Координаты вершин трапеции для пространственного преобразования
arc = np.float32([[20, 200],
                  [350, 200],
                  [275, 120],
                  [85, 120]])
arc_draw = np.array(arc, dtype=np.int32)
# Координаты вершин прямоугольника, в который преобразуется трапеция 
dst = np.float32([[0, img_size[1]],
                  [img_size[0], img_size[1]],
                  [img_size[0], 0],
                  [0, 0]])

# В цикле организовано чтение кадра с камеры, его анализ и отправка 
# управляющего сигнала сервоприводу и драйверу двигателя
while (cv.waitKey(1) != 27):
	# Чтение кадра
    ret, frame = cap.read()
    if ret == False:
        print("End")
        break

	# изменение размера кадра и бинаризация по порогу. 
    resized = cv.resize(frame, (img_size[0], img_size[1]))

    hls = cv.cvtColor(resized, cv.COLOR_BGR2HLS)
    allBinary = cv.inRange(hls, (0,245,0), (255,255,255))
	#	В итоге получается чёрнобелое изображение на котором линии 
    # разметки белые, а всё остальное чёрное. Теперь пиксели линии 
    # разметки можно детектировать по цвету.
    allBinary_visual = allBinary.copy()
    cv.polylines(allBinary_visual, [arc_draw], True, 255)

	# Всё изображение нам не требуется, совершаем перспективное 
    # преобразование, чтобы осталась только область непосредственно 
    # перед колёсами автомобиля и парралельные линии дорожной разметики 
    # были парралельными и на изображении, а не сходящимися в одну точку.
    matrix = cv.getPerspectiveTransform(arc, dst)
    warp = cv.warpPerspective(allBinary, matrix, (img_size[0], img_size[1]), 
        flags=cv.INTER_LINEAR)

	# высчитываем координаты самого белого столбца в двух нижних четвертях 
    # изображения. Именно по этим координатам мы начнём искать пиксели разметки.
    histogram = np.sum(warp[warp.shape[0] // 2:, :], axis=0)
    mid = histogram.shape[0] // 2
    r_index = np.argmax(histogram[:mid])
    l_index = np.argmax(histogram[mid:]) + mid
    warp_visual = warp.copy()

	# По найденным координатам, начиная от низа изображения, располагаем 
    # прямоугольные области. Все белые пиксели попадающие в область считаются 
    # пикселями линий разметки. От размера прямоугольных областей, их 
    # колличества зависит применимость алгоритма к тем или иным условиям.

    n_windows = 9
    window_height = np.int(warp.shape[0] / n_windows)
    windows_half = 25

    x_lcenter = l_index
    x_rcenter = r_index

    left_lane = np.array([], dtype=np.int16)
    right_lane = np.array([], dtype=np.int16)

    out_img = np.dstack((warp, warp, warp))

    non_zero = warp.nonzero()
    whitePixelY = np.array(non_zero[0])
    whitePixelX = np.array(non_zero[1])
	# вычисляем координаты прямоугольной области, каждая следующая 
    # располагается над предыдущей
    for window in range(n_windows):
        win_y1 = warp.shape[0] - (window + 1) * window_height
        win_y2 = warp.shape[0] - (window) * window_height

        left_win_x1 = x_lcenter - windows_half
        left_win_x2 = x_lcenter + windows_half
        right_win_x1 = x_rcenter - windows_half
        right_win_x2 = x_rcenter + windows_half

# Запоминаем белые пиксели в области
        good_left_indexs = ((whitePixelY >= win_y1) & (whitePixelY <= win_y2) 
            & (whitePixelX >= left_win_x1) & 
            (whitePixelX <= left_win_x2)).nonzero()[0]
        good_right_indexs = ((whitePixelY >= win_y1) & 
            (whitePixelY <= win_y2) & (whitePixelX >= right_win_x1) 
            & (whitePixelX <= right_win_x2)).nonzero()[0]

        left_lane = np.concatenate((left_lane, good_left_indexs))
        right_lane = np.concatenate((right_lane, good_right_indexs))
# Если белых пикселей в области достаточно много, то заносим их в 
# список принадлежащих к линиям разметки
        if len(good_left_indexs) > 50:
            x_lcenter = np.int(np.mean(whitePixelX[good_left_indexs]))
        if len(good_right_indexs) > 50:
            x_rcenter = np.int(np.mean(whitePixelX[good_right_indexs]))

    out_img[whitePixelY[left_lane], whitePixelX[left_lane]] = [255, 0, 0]
    out_img[whitePixelY[right_lane], whitePixelX[right_lane]] = [0, 255, 0]

    leftx = whitePixelX[left_lane]
    lefty = whitePixelY[left_lane]
    rightx = whitePixelX[right_lane]
    righty = whitePixelY[right_lane]

# как только все пиксели принадлежащие разметке найдены, с помощью МНК 
# получаем уравнение парабол совпадающих с линиями разметки. И вычисляяем 
# уравнение центральной линии нашей полосы движения. 
    try:
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)
        center_fit = ((left_fit + right_fit) / 2)
    except TypeError:
        if center_fit[-1] - center_fit[0] > 10:
            control(pi, ESC, 1500, STEER, 75)
        elif center_fit[-1] - center_fit[0] < -10:
            control(pi, ESC, 1500, STEER, 75)
        else:
            control(pi, ESC, 1500, STEER, 75)
        continue

    for ver_ind in range(out_img.shape[0]):
        gor_ind = (center_fit[0] * (ver_ind ** 2) +
                   center_fit[1] * ver_ind +
                   center_fit[2])
# Управляющий сигнал для сервопривода будет тем больше, чем сильнее 
# отклонение центральной линии дороги от центральной вертикали нашего изображения.

    down = center_fit[-1]
    up = center_fit[0]
    dist = int(up - down) + 180
    a = int(dist * 0.3)
    if a > 10 and a < 20:
        print("slow left")
        control(pi, ESC, 1390, STEER, 85)
    elif a > 20:
        print("left")
        control(pi, ESC, 1390, STEER, 95)
    elif a < -10 and a > -20:
        print("slow right")
        control(pi, ESC, 1390, STEER, 65)
    elif a < -20:
        print("right")
        control(pi, ESC, 1390, STEER, 55)
    else:
        print("forward")
        control(pi, ESC, 1390, STEER, 75)