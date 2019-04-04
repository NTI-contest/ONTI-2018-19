import math
import sys


def gauss(polygon):
    # polygon в формате [(x1,y1),...(xi,yi)] или [[x1,y1], ... [xi,yi]]
    polygon.append(polygon[0])
    S = 0
    for i in range(len(polygon) - 1):
        S += polygon[i][0] * polygon[i + 1][1]      # Xi * Yi+1
        S -= polygon[i][1] * polygon[i + 1][0]      # Yi * Xi+1
    S = abs(S) * 0.5
    return int(S)


def circles(lst):
    a1, b1, r1, a2, b2, r2, a3, b3, r3 = lst
    # расстояние между центрами маяков M1 (a1, b1), M2 (a2, b2)
    d = math.sqrt((a2 - a1) ** 2 + (b2 - b1) ** 2)

    if d >= r1 + r2 or d < abs(r1-r2):
        return False

    d2 = (r2 ** 2 - r1 ** 2) / (2 * d) + (d / 2)
    d1 = d - d2

    h = math.sqrt(r1 ** 2 - d1 ** 2)
    k = d1 / d2

    xs = (a1 + k * a2) / (1 + k)
    ys = (b1 + k * b2) / (1 + k)

    x1 = (h / d) * (b1 - b2) + xs
    y1 = (h / d) * (a2 - a1) + ys

    x2 = -(h / d) * (b1 - b2) + xs
    y2 = -(h / d) * (a2 - a1) + ys

    test1 = int(math.sqrt((x1 - a3) ** 2 + (y1 - b3) ** 2))
    test2 = int(math.sqrt((x2 - a3) ** 2 + (y2 - b3) ** 2))

    if abs(test1 - r3) <= abs(test2 - r3):
        return (x1, y1)
    else:
        return (x2, y2)

    
data = sys.stdin.readlines()

K, N, dT = list(map(int, data[0].strip().split(' ')))
data.pop(0)
"""
K  - кол-во маяков
N  - кол-во замеров
dT - пауза между замерами, мс
"""

beacons, measures = [], []

for i in range(K):
    beacons.append(list(map(float, data[i].strip().split(' '))))

for i in range(N):
    measures.append(list(map(float, data[i + K].strip().split(' '))))

xy_obstacle, xy_robot = [], []
alpha = 0

for i in range(N):
    b_idx = []
    for b in range(len(beacons)):
        if measures[i][b + 1] >= 0:
            b_idx.append(b)
        if len(b_idx) == 3:
            break

    b_info = []
    for  idx in b_idx:
        b_info.append(beacons[idx][1])
        b_info.append(beacons[idx][2])
        b_info.append(measures[i][idx + 1])

    xy = circles(b_info)
    xy_robot.append(xy)

    if (measures[i][0] < 1000) and len(xy_robot) > 1:              # замеры с дальномера
        dY = xy_robot[-1][1] - xy_robot[-2][1]
        dX = xy_robot[-1][0] - xy_robot[-2][0]
        alpha = (math.atan2(dY, dX))

        betta = alpha + math.radians(90)
        xy = [xy_robot[-1][0] + measures[i][0] * math.cos(betta), xy_robot[-1][1] + measures[i][0] * math.sin(betta)]

        xy_obstacle.append(xy)

print(gauss(xy_obstacle))
