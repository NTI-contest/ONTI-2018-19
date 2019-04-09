import cv2
from random import randint
import numpy as np


def image_diff(image1, image2, threshold=0):
    difference = 0
    for i in range(100):
        x = randint(0, image1.shape[0] - 1)
        y = randint(0, image1.shape[1] - 1)
        z = randint(0, image1.shape[2] - 1)
        difference += abs(image1[x, y, z] - image2[x, y, z]) > threshold
    return difference


vidcap = cv2.VideoCapture('154.mp4')
success, image = vidcap.read()
prev_image = image

frames = []
old_frame = 0
unique_images = []
last_image = 0
while success:
    success, image = vidcap.read()
    # добавляем корректную обработку последнего изображения
    if not success:
        image = np.zeros(prev_image.shape, np.uint8)
    frames.append(image)

    diff = image_diff(prev_image, image)
    # если кадры различаются более чем на 30%, значит на кадре уже другое изображение
    if diff > 30:
        unique_found = True
        # для того, чтобы сравнивать изображения, возьмем самый стабильный кадр
        stable_image = frames[(len(frames) + old_frame) // 2]
        old_frame = len(frames)
        # проверяем, есть ли в массиве уникальных кадров данное изображение
        for unique_image in unique_images:
            diff = image_diff(stable_image, unique_image, 3)
            if diff < 50:
                unique_found = False
                break
        if unique_found:
            unique_images.append(stable_image)
    prev_image = image

print(len(unique_images))
