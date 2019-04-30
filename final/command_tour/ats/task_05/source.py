import cv2
import numpy

i = 1
# В цикле перебираем имеющиеся изображения
while (i<6):
    frame = cv2.imread(str(i) + ".jpg")
# Приводим все изображения к стандартному виду
    frame = cv2.resize(frame, (60, 120))
    cv2.imshow(str(i), frame)
# обрезаем края изображения, чтобы избавиться от фона, оставшегося 
# после детектирования.
    cutedFrame = frame[20:101, 8:52] #получилось изображение 44 на 81 пиксель
    cv2.imshow("cutedFrame", cutedFrame)
# переводим изображение в цветовое пространство HSV
    hsv = cv2.cvtColor(cutedFrame, cv2.COLOR_BGR2HSV)
# Оставляем составляющую, отвечающую за яркость пикселя.
    v = hsv[:, :, 2]
    cv2.imshow("v " + str(i), v)
# Считаем сумму яркости пикселей в трех областях, каждая соответствует 
# своему сигналу светофора.
    red_sum_brightness = numpy.sum(v[0:27, 0:44])
    cv2.imshow("red", v[0:27, 0:44])
    yellow_sum_brightness = numpy.sum(v[28:54, 0:44])
    cv2.imshow("yell",v[27:54, 0:44])
    green_sum_brightness = numpy.sum(v[55:81, 0:44])
    cv2.imshow("gre", v[55:81, 0:44])


# По области в которой яркость максимальна мы судим о сигнале светофора
    if green_sum_brightness > yellow_sum_brightness and 
		green_sum_brightness > red_sum_brightness:
        predicted_label = [0, 0, 1]
    elif yellow_sum_brightness > green_sum_brightness and 
		yellow_sum_brightness > red_sum_brightness:
        predicted_label = [0, 1, 0]
    elif red_sum_brightness > green_sum_brightness and 
		red_sum_brightness > yellow_sum_brightness:
        predicted_label = [1, 0, 0]
    else:
        predicted_label = [0, 1, 0]
    print(str(red_sum_brightness) + " : " + str(yellow_sum_brightness) + 
		" : " + str(green_sum_brightness))
    print(predicted_label)

    key = cv2.waitKey(1)
    if key == ord("n"):
        i = i+1
        cv2.destroyAllWindows()

    if key == ord("q"):
        break

cv2.destroyAllWindows()