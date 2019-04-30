import math
# import matplotlib.pyplot as plt

import numpy as np


def haversine(coord1, coord2):
    lon1 = coord1[0]
    lon2 = coord2[0]
    lat1 = coord1[1]
    lat2 = coord2[1]
    EARTH_RADIUS = 6371000

    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) 
    * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    dec_m = EARTH_RADIUS * c
    return dec_m


def points_in_rad(center_coord, arr, radius=2000):
    """
    Получение всех точек в определенном радиусе от центральной
    :param center_coord: центральная точка
    :param arr: массив точек
    :param radius: радиус в метрах
    :return: список точек
    """
    sorted_arr = sorted(arr)

    pointsInRadius = []

    for i in range(0, len(sorted_arr)):
        if haversine((center_coord), sorted_arr[i]) <= radius:
            pointsInRadius.append(sorted_arr[i])
    return pointsInRadius


def angle_between_points(left, center, right):
    """
    Расчет угла между тремя точками на поверхности Земли в радианах
    """
    a = haversine(center, right)
    b = haversine(center, left)
    c = haversine(left, right)
    return math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))


def destination_point(center_coord, distance, angle):
    """
    Вычисляет точку на поверхности Земли, удаленную от определенной на расстояние
    :param center_coord: центральная точка, относительно которой мы ищем
    :param distance: расстояние в метрах
    :param angle: угол в градусах
    :return: точку, удаленную на distance с углом angle
    """
    distance /= 6371000
    angle = math.radians(angle)
    lng1, lat1 = map(math.radians, center_coord)
    lat2 = math.asin(math.sin(lat1) * math.cos(distance) +
                     math.cos(lat1) * math.sin(distance) * math.cos(angle))
    lng2 = lng1 + math.atan2(math.sin(angle) * math.sin(distance) * math.cos(lat1),
                             math.cos(distance) - math.sin(lat1) * math.sin(lat2))
    return math.degrees(lng2), math.degrees(lat2)


def points_in_sector(center_coord, arr, radius=2000, angle=90, step=1):
    """
    Получаем максимальное количество точек, находящиеся в секторе
    :param center_coord: центральная точка
    :param arr: массив точек
    :param radius: радиус в метрах
    :param angle: угол в градусах
    :param step: шаг для определения сектора
    :return: список точек
    """
    points = points_in_rad(center_coord, arr, radius)

    max_points = []

    angle = math.radians(angle)

    start_points = []
    start_angle = 0.0
    while start_angle < 360:
        start_points.append(destination_point(center_coord, radius, start_angle))
        start_angle += step

    for start_point in start_points:
        tmp_points = []
        for point in points:
            if angle_between_points(start_point, center_coord, point) <= angle / 2:
                tmp_points.append(point)
        if len(tmp_points) > len(max_points):
            max_points = tmp_points
    # print('LOOOOOOOOL')
    return max_points


arr = [(104.2607150000, 52.2509700000),
       (104.3047200000, 52.2876890000),
       (104.2963780000, 52.2908390000),
       (104.2807670000, 52.2834890000),
       (104.2899250000, 52.2738040000),
       (104.2899250000, 52.2738040000),
       (104.2920600000, 52.2732450000),
       (104.2672810000, 52.2513130000),
       (104.2921130000, 52.2742630000),
       (104.2852950000, 52.2773480000),
       (104.2805530000, 52.2779920000),
       (104.2992640000, 52.2784380000),
       (104.2987450000, 52.2785310000),
       (104.2839000000, 52.2787930000),
       (104.2839430000, 52.2784510000),
       (104.2934170000, 52.2985000000),
       (104.2866900000, 52.2892410000),
       (104.2831170000, 52.2918110000),
       (104.2945860000, 52.3006260000),
       (104.2776020000, 52.2751160000),
       (104.2884280000, 52.2935860000)]

sorted_arr = sorted(arr)
max_points_in_radius = 0

max_coord_r = ()

max_lon = max(list(zip(*arr))[0])

lon = min(list(zip(*arr))[0])
lat = min(list(zip(*arr))[1])
center_coord = (lon, lat)

for i in range(0, 1000):
    if lon - max_lon > 0.1:
        break
    lon += 0.01
    lat = 52.23
    points_in_radius = 0
    ps = 0
    for j in range(0, 1000):
        lat += 0.01
        center_coord = (lon, lat)

        if center_coord in arr:
            pass
        else:
            points_in_radius = len(points_in_sector(center_coord, arr))

        if points_in_radius > max_points_in_radius:
            max_points_in_radius = points_in_radius
            max_coord_r = center_coord

max_lon = max(list(zip(*arr))[0])
max_lat = max(list(zip(*arr))[1])

print(max_coord_r)
print(max_points_in_radius)

# Проверка правильности работы алгоритма расположения точек по окружности
# start_points = []
# start_angle = 0.0
# while start_angle < 360:
#     start_points.append(
#    destination_point((104.2805530000, 52.2779920000), 2000, start_angle))
#     start_angle += 10
#
# print('\n'.join(map(str, map(lambda p: ','.join(map(str, p[::-1])), start_points))))