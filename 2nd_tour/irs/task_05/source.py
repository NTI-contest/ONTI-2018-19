# -*- coding: utf-8 -*-
import sys

def hex2ip(hex_num):
    #формат входного IP-адреса:     FFFFFFFF
    #формат выходного IP-адреса:    255.255.255.255
    ip = []
    for i in range(0, len(hex_num), 2):
        ip.append(int(hex_num[i: i + 2], 16))
    return '.'.join(map(str, ip))

def cross(coords):
    x1, y1, x2, y2, x3, y3, x4, y4 = coords
    v2 = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    v3 = (x2 - x1) * (y4 - y1) - (y2 - y1) * (x4 - x1)
    v0 = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    v1 = (x4 - x3) * (y2 - y3) - (y4 - y3) * (x2 - x3)
    return ((v2 < 0 and v3 > 0) or (v2 > 0 and v3 < 0)) and \
           ((v0 < 0 and v1 > 0) or (v0 > 0 and v1 < 0))

data = sys.stdin.readlines()

packets = int(data[0].strip())      # кол - во переданных пакетов
times = []                          # время в мс, в которое были сняты координаты
coord_x = []                         # координаты оси Х положения робота в момент times[]
coord_y = []                         # координаты оси Y положения робота в момент times[]
ip_sender = []                       # IP отправителя

for i in range(packets):
    ip_sender.append(data[i+1].strip()[0:8])
    times.append( int(data[i+1].strip()[40: 48], 16))
    coord_x.append(int(data[i+1].strip()[48: 56], 16))
    coord_y.append(int(data[i+1].strip()[56: 64], 16))

data0 = []
data_by_ip = {}
for i in range(packets):
    ip_out, t, x, y = ip_sender[i], times[i], coord_x[i], coord_y[i]
    data0.append((t, ip_out, x, y))

data = sorted(data0)

for i in range(0, len(data)):
    if data[i][1] not in data_by_ip:
        data_by_ip[data[i][1]] = [data[i]]
    else:
        data_by_ip[data[i][1]].append(data[i])

crosses = []
for key1 in data_by_ip:
    for key2 in data_by_ip:
        if key1 == key2:
            break
        for k1 in range(1, len(data_by_ip[key1])):
            x1y1 = data_by_ip[key1][k1 - 1][2:]
            x2y2 = data_by_ip[key1][k1][2:]

            for k2 in range(1, len(data_by_ip[key2])):
                x3y3 = data_by_ip[key2][k2 - 1][2:]
                x4y4 = data_by_ip[key2][k2][2:]

                if cross(x1y1 + x2y2 + x3y3 + x4y4):
                    keys = sorted((key1, key2))
                    if keys not in crosses:
                        crosses.insert(0, keys)

if len(crosses) == 0:
    print (-1)
else:
    for i in range(len(crosses)):
        print (*([hex2ip(crosses[i][0]), hex2ip(crosses[i][1])]))

