n, m = map(int, input().split())

s = []
for i in range(n):
    s.append(input())

dist = [[[2000000000 for j in range(4)] for i in range(m)] for k in range(n)]
qi = [0] * (n * m * 4)
qj = [0] * (n * m * 4)
qd = [0] * (n * m * 4)
ql = 0
qr = 0

for i in range(n):
    for j in range(m):
        if (s[i][j] == 's'):
            dist[i][j][0] = 0
            qi[qr] = i
            qj[qr] = j
            qd[qr] = 0
            qr += 1
            break
    if qr > 0:
        break

ans = -1
while ql < qr:
    i = qi[ql]
    j = qj[ql]
    d = qd[ql]
    ql += 1

    if s[i][j] == 'f':
        ans = dist[i][j][d]
        break

    if d == 0:
        if i + 1 < n and s[i + 1][j] != '#' and dist[i + 1][j][d] > dist[i][j][d] + 1:
            dist[i + 1][j][d] = dist[i][j][d] + 1
            qi[qr] = i + 1
            qj[qr] = j
            qd[qr] = d
            qr += 1
    elif d == 1:
        if j > 0 and s[i][j - 1] != '#' and dist[i][j - 1][d] > dist[i][j][d] + 1:
            dist[i][j - 1][d] = dist[i][j][d] + 1
            qi[qr] = i
            qj[qr] = j - 1
            qd[qr] = d
            qr += 1
    elif d == 2:
        if i > 0 and s[i - 1][j] != '#' and dist[i - 1][j][d] > dist[i][j][d] + 1:
            dist[i - 1][j][d] = dist[i][j][d] + 1
            qi[qr] = i - 1
            qj[qr] = j
            qd[qr] = d
            qr += 1
    elif d == 3:
        if j + 1 < m and s[i][j + 1] != '#' and dist[i][j + 1][d] > dist[i][j][d] + 1:
            dist[i][j + 1][d] = dist[i][j][d] + 1
            qi[qr] = i
            qj[qr] = j + 1
            qd[qr] = d
            qr += 1

    if dist[i][j][(d + 1) % 4] > dist[i][j][d] + 1:
        dist[i][j][(d + 1) % 4] = dist[i][j][d] + 1
        qi[qr] = i
        qj[qr] = j
        qd[qr] = (d + 1) % 4
        qr += 1

    if dist[i][j][(d + 3) % 4] > dist[i][j][d] + 1:
        dist[i][j][(d + 3) % 4] = dist[i][j][d] + 1
        qi[qr] = i
        qj[qr] = j
        qd[qr] = (d + 3) % 4
        qr += 1

print(ans)