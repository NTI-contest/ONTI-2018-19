def dsu_init(n):
    for i in range(n):
        p[i] = i
    return


def dsu_get(v):
    if v != p[v]:
        p[v] = dsu_get(p[v])
    return p[v]


def dsu_union(a, b):
    a = dsu_get(a)
    b = dsu_get(b)
    if a != b:
        map_union(a, b)
    return


def map_union(a, b):
    if len(mp[b]) > len(mp[a]):
        map_union(b, a)
        return

    global cur
    cur += cnt[a] * cnt[b]
    p[b] = a
    cnt[a] += cnt[b]
    for i in mp[b]:
        mp[a].setdefault(i, 0)
        cur -= mp[b][i] * mp[a][i]
        mp[a][i] += mp[b][i]
    return


n = int(input())
c = [int(i) for i in input().split()]

p = [0] * n
cnt = [0] * n
mp = [{} for i in range(n)]
cur = 0

for i in range(n):
    mp[i][c[i]] = 1
    cnt[i] += 1

a = [0] * (n - 1)
b = [0] * (n - 1)
for i in range(n - 1):
    a[i], b[i] = [int(i) - 1 for i in input().split()]

q = [int(i) - 1 for i in input().split()]
q.reverse()

dsu_init(n)
ans = [0]
for i in q:
    dsu_union(a[i], b[i])
    ans.append(cur)

ans.reverse()
print(' '.join(map(str, ans)))
