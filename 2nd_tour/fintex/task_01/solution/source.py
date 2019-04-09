import numpy as np
from functools import reduce

first = lambda x: sum(x) // 3
second = lambda x: int(0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2])
third = lambda x: (min(x) + max(x)) // 2
forth = lambda x: max(x)
first_filter = lambda i, j, k, picture: int((reduce(lambda x, y: x * y,
                            picture[i - 1:i + 2, j - 1:j + 2, k].flatten())) ** (1 / 9))
second_filter = lambda i, j, k, picture: 
                             sorted(picture[i - 1:i + 2, j - 1:j + 2, k].flatten())[4]


def apply_filter(picture: np.ndarray, f):
    ans = picture.copy()
    for k in range(3):
        for i in range(1, picture.shape[0] - 1):
            for j in range(1, picture.shape[1] - 1):
                ans[i, j, k] = f(i, j, k, picture)
    return ans


def convert(picture, converter):
    return np.array(list(map(converter, picture.reshape((-1, 3)))))


w, h = map(int, input().split())
str_pixels = input()
filter_num = int(input())
converter_num = int(input())

a_pixels = map(lambda x: 
            (int(x[:2], 16), int(x[2:4], 16), int(x[4:6], 16)), str_pixels.split())
a_pixels = list(a_pixels)
picture = np.array(a_pixels, dtype=object)
picture.resize((h, w, 3))

picture = apply_filter(picture, first_filter if filter_num == 1 else second_filter)
picture = convert(picture,
                  first if converter_num == 1 else second if converter_num == 2
                  else third if converter_num == 3 else forth)

print(min(picture), max(picture))