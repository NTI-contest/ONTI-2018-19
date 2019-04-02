def renew(pairs):
    res = []
    for p in pairs:
        if p[0] < -360:
            res.append((-360, p[1]))
            res.append((720 + p[0], 360))
        elif p[1] > 360:
            res.append((-360, p[1] - 720))
            res.append((p[0], 360))
        else:
            res.append(p)
     
    pairs = []
   
    
    return res


n, gamma = map(int, input().split())
gamma *= 2

lines = [input().split() for _ in range(n)]

pairs = [(2 * int(x[1]) - int(x[2]), 2 * int(x[1]) + int(x[2])) for x in lines]

pairs = renew(pairs)
pairs.sort(key=lambda tup: tup[0])

log = ''
cnt = 0
l, r = pairs[0]

for p in pairs[1:]:
    if p[0] <= r:
        if p[1] > r:
            r = p[1]
    else:
        cnt += (p[0] - r + gamma - 1) // gamma
        r = p[1]

cnt += (720 + l - r + gamma - 1) // gamma

print(cnt)