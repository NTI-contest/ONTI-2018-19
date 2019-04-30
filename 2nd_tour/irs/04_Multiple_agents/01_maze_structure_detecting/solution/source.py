# -*- coding: utf-8 -*-
import sys

def write_matrix(cell1, cell2, value):
    global matrix
    matrix[cell1][cell2] = int(not value)
    matrix[cell2][cell1] = int(not value)

def edit_matrix(m):
    global LMooved

    for rr in range(N):
        x, y, az = robots_moves[rr]
        cells = [0, 0, 0]                      # sensors: [left, forward, right]
        if az == 0:
            cells[0] = coord2cell(x - 1, y)
            cells[1] = coord2cell(x, y - 1)
            cells[2] = coord2cell(x + 1, y)
        elif az == 1:
            cells[0] = coord2cell(x, y - 1)
            cells[1] = coord2cell(x + 1, y)
            cells[2] = coord2cell(x, y + 1)
        elif az == 2:
            cells[0] = coord2cell(x + 1, y)
            cells[1] = coord2cell(x, y + 1)
            cells[2] = coord2cell(x - 1, y)
        elif az == 3:
            cells[0] = coord2cell(x, y + 1)
            cells[1] = coord2cell(x - 1, y)
            cells[2] = coord2cell(x, y - 1)

        robot_obstacle = [False] * 3
        for b in range(N):                                  # проверяем каждого робота
            for ss in range(3):                             # на пересечение с каждым дальномером
                if coord2cell(robots_moves[b][0], robots_moves[b][1]) == cells[ss]:
                    robot_obstacle[ss] = True

        cell = coord2cell(x, y)
        for s in range(3):                                  # 3 sensors
            if cells[s] >= K * M or cells[s] < 0:
                continue

            if not robot_obstacle[s]:
                write_matrix(cell, cells[s], measures[rr][m][s + 1])
                write_matrix(cells[s], cell, measures[rr][m][s + 1])

            if not robot_obstacle[s] and not measures[rr][m][s + 1]:
                LMooved[cells[s]] = True

def cell2coord(cell):
    y = int(cell / K)
    x = cell - y * K
    return (x, y)

def coord2cell(x, y):
    # K - ширина лабиринта, секторов
    return y * K + x

def bfs():
    start = coord2cell(robots[0][0], robots[0][1])
    visited = [False for i in range(K * M)]

    path = []
    queue = [start]
    while len(queue) > 0:
        p = queue.pop(0)
        if not visited[p]:
            visited[p] = True
            path.append(p)

            for i in range(K * M):
                if not visited[i] and matrix[p][i] > 0:
                    queue.append(i)

            x, y = cell2coord(p)
            if x + 1 < K:
                if matrix[p][p + 1] < 0 and not LMooved[p + 1]:
                    return []

            if x - 1 >= 0:
                if matrix[p][p - 1] < 0 and not LMooved[p - 1]:
                    return []

            if y + 1 < M:
                if matrix[p][p + K] < 0 and not LMooved[p + K]:
                    return []

            if y - 1 >= 0:
                if matrix[p][p - K] < 0 and not LMooved[p - K]:
                    return []

    return path

data = sys.stdin.readlines()
N, K, M, cnt_sens = list(map(int, data[0].strip().split(' ')))
data.pop(0)

#N        - кол-во роботов на поле
#K        - ширина лабиринта, секторов
#M        - длина лабиринта, секторов
#cnt_sens - кол-во показаний датчиков

measures, robots = [], []
az = ['U','R','D','L']
for i in range(N):
    line = data[0].strip().split(' ')
    robots.append([int(line[0]), int(line[1]), az.index(line[2])])
    data.pop(0)

for move in range(N):
    measures.append([])
    for m in range(cnt_sens):
        line = data[move * cnt_sens + m].strip().split(' ')
        measures[-1].append([line[0]])
        for i in range(3):
            measures[-1][-1].append(int(line[i + 1]))

matrix = [[-1 for j in range(K*M)] for i in range(K*M)]     # пустая матрица смежности
move_cells = [1 for i in range(N)]                          # подсчет посещенных клеток роботами
LMooved = [False for i in range(K * M)]			            # просмотренные или посещенные клетки

robots_moves = []
for i in range(N):
    robots_moves.append(robots[i])                          # стартовые позиции роботов

for m in range(cnt_sens):
    for r in range(N):
        x, y, azimut = robots_moves[r]
        LMooved[coord2cell(x, y)] = True

        action = measures[r][m][0]
        if action == 'L':   azimut -= 1
        elif action == 'R': azimut += 1
        azimut %= 4

        if action == 'F':
            x0, y0 = x, y
            if   azimut == 0: y -= 1
            elif azimut == 1: x += 1
            elif azimut == 2: y += 1
            elif azimut == 3: x -= 1
            move_cells[r] += 1

            write_matrix(coord2cell(x,y),coord2cell(x0,y0), 0)

        robots_moves[r] = [x, y, azimut]

    edit_matrix(m)

result = bfs()
if len(result) == 0 :
    print (move_cells[0])
else:
    print (len(result))
