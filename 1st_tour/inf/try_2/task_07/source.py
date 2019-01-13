import sys

def dist(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2

def max_diag(l):
    a1 = (l[4] - l[0]) ** 2 + (l[5] - l[1]) ** 2
    a2 = (l[6] - l[2]) ** 2 + (l[7] - l[3]) ** 2
    return max(a1, a2)


dataset = sys.stdin.read()

p = [int(a) for a in dataset.split()]
q = [0] * 3

q[0] = p[:]
q[1] = p[:]
q[2] = p[:]

v = [[p[(2 * x + 2) % 6] + p[(2 * x + 4) % 6] - p[(2 * x + 6) % 6],  p[(2 * x + 3) % 6] + p[(2 * x + 5) % 6] - p[(2 * x + 1) % 6]] for x in range(3)]

max_value = 0
for i in range(3):
    q[i] = q[i][: ((i + 2) * 2) % 6] + v[i] + q[i][((i + 2) * 2) % 6:]
    max_value = max(max_value, max_diag(q[i]))

ansp = []

for i in range(3):  
    if max_value == max_diag(q[i]):
        ansp.append(v[i])

ans = []
max_sum = 0

if len(ansp) == 2:
    if sum(ansp[0]) > sum(ansp[1]):
        ans = ansp[0]
    elif sum(ansp[0]) < sum(ansp[1]):
        ans = ansp[1]
    elif ansp[0][0] > ansp[1][0]:
        ans = ansp[0]
    else:
        ans = ansp[1]
else:
    ans = ansp[0]

print('{} {}'.format(ans[0], ans[1]))
        