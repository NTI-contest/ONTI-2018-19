def get_p(v, p):
    if v == p[v]:
        return v
    p[v] = get_p(p[v], p)
    return p[v]


def union(a, b, p, size):
    a = get_p(a, p)
    b = get_p(b, p)

    if a != b:
        if size[a] > size[b]:
            p[b] = a
            size[a] += size[b]
        else:
            p[a] = b
            size[b] += size[a]


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


a, b, d = map(int, input().split())
n, m = map(int, input().split())

positions = [tuple(map(int, input().split())) for i in range(n)]

size = [1 for i in range(n)]
p = [i for i in range(n)]

for i in range(m):
    n1, n2 = map(int, input().split())
    n1 -= 1
    n2 -= 1

    if dist(positions[n1], positions[n2]) <= d:
        union(n1, n2, p, size)


common_p = get_p(0, p)
all_have_common_p = True
for i in range(1, n):
    if get_p(i, p) != common_p:
        all_have_common_p = False
        break

if all_have_common_p:
    print("YES")
else:
    print("NO")
