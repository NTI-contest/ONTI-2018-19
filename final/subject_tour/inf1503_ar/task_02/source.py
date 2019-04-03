# put your python code here

def neighbours(i, j):
    return [i-1, j], [i+1, j], [i, j-1], [i, j+1]


def label_area(m, i, j, label):
    m[i][j] = label
    for ni, nj in neighbours(i, j):
        if m[ni][nj] == 1:
            label_area(m, ni, nj, label)

h, w = map(int, input().split())
m = []

for i in range(h):
    line = map(int, input().split())
    m.append(list(line))

label = 2
for i in range(h):
    for j in range(w):
        if m[i][j] == 1:
            label_area(m, i, j, label)
            label += 1

areas = {}

for i in range(h):
    for j in range(w):
        value = m[i][j]
        if value != 0:
            if value not in areas:
                areas[value] = 1
            else:
                areas[value] += 1

for area in sorted(areas.values()):
    print(area)


