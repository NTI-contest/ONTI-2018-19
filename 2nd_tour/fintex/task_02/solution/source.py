import math

n, m = map(int, input().split())

arr = [None] * n
for i in range(m):
    arr[i] = [None] * m

for i in range(m):
    line = input().split()
    for j in range(n):
        r, g, b = int(line[j][:2], 16), int(line[j][2:4], 16), int(line[j][4:], 16)
        arr[j][i] = round((r + g + b) / 3)

w = 200
w8 = w // 8
h = 200
h8 = h // 8
nbins = 18
angle_per_bin = 2 * math.pi / nbins
angle_shift = angle_per_bin / 2

blocks = [None] * w8
for i in range(w8):
    blocks[i] = [None] * h8
    for j in range(h8):
        blocks[i][j] = [0] * nbins

blocks2 = [None] * w8
for i in range(w8):
    blocks2[i] = [None] * h8
    for j in range(h8):
        blocks2[i][j] = [0] * nbins

for i in range(w):
    for j in range(h):
        i1 = i - 1 if i > 0 else i
        i2 = i + 1 if i < w - 1 else i
        j1 = j - 1 if j > 0 else j
        j2 = j + 1 if j < h - 1 else j

        x = arr[i2][j] - arr[i1][j]
        y = arr[i][j2] - arr[i][j1]

        angle = 2 * math.pi + math.atan2(y, x)
        lower = (angle - angle_shift) // angle_per_bin
        upper = lower + 1

        mag = math.sqrt(x ** 2 + y ** 2)
        mag_upper = ((angle - angle_shift) % angle_per_bin) / angle_per_bin * mag
        mag_lower = mag - mag_upper

        blocks[i // 8][j // 8][int(lower % nbins)] += mag_lower
        blocks[i // 8][j // 8][int(upper % nbins)] += mag_upper

for i in range(w8 - 1):
    for j in range(h8 - 1):
        vector_len = 0
        for q in range(nbins):
            vector_len += blocks[i][j][q] ** 2
            vector_len += blocks[i + 1][j][q] ** 2
            vector_len += blocks[i][j + 1][q] ** 2
            vector_len += blocks[i + 1][j + 1][q] ** 2
        vector_len = math.sqrt(vector_len)

        for w in range(nbins):
            blocks2[i][j][w] = blocks2[i][j][w] + 0 if vector_len == 0 else\
                (blocks[i][j][w] / vector_len)
            blocks2[i + 1][j][w] = blocks2[i + 1][j][w] + 0 if vector_len == 0 else\
                (blocks[i + 1][j][w] / vector_len)
            blocks2[i][j + 1][w] = blocks2[i][j + 1][w] + 0 if vector_len == 0 else\
                (blocks[i][j + 1][w] / vector_len)
            blocks2[i + 1][j + 1][w] = blocks2[i + 1][j + 1][w] + 0 if vector_len == 0\
                else (blocks[i + 1][j + 1][w] / vector_len)

hor, ver = 0, 0
for i in range(w8):
    for j in range(h8):
        ans = (0, 0)
        for q in range(nbins):
            ans = (ans[0] + blocks2[i][j][q] * math.cos(angle_per_bin * q + angle_shift),
                   ans[1] + blocks2[i][j][q] * math.sin(angle_per_bin * q + angle_shift))

        if math.fabs(ans[0]) - math.fabs(ans[1]) > 0:
            ver += 1
        elif math.fabs(ans[1]) - math.fabs(ans[0]) > 0:
            hor += 1

if hor / (ver + 1) > 1.3:
    print(2)
elif ver / (hor + 1) > 1.3:
    print(1)
else:
    print(0)
