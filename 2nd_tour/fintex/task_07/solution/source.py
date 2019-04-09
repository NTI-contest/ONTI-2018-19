import cv2
import numpy as np


# алгоритм хэширования по среднему,
# на вход подается массив пикселей в виде (r, g, b),
# на выходе получается число, являющееся цифровым представлением изображения
def average_hash(image):
    resized_grey = cv2.cvtColor(cv2.resize(image, (12, 12)), cv2.COLOR_BGR2GRAY)
    pixels = np.asarray(resized_grey)
    average = pixels.mean()
    difference = pixels > average
    return sum([2 ** (i % 8) for i, v in enumerate(difference.flatten()) if v])


vidcap = cv2.VideoCapture('1.mp4')
success, image = vidcap.read()
count = 0
prev_hash = average_hash(image)
while success:
    new_hash = average_hash(image)
    # если хэши отличаются, значит на кадре уже другое изображение
    if prev_hash != new_hash:
        count += 1
    prev_hash = new_hash
    success, image = vidcap.read()
print(count)
