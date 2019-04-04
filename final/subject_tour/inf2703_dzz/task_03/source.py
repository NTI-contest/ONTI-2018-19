def count(pairs, x):
    cnt = -1
    
    for p in pairs:
        if abs(p[1] - x[1]) <= 160 or abs(p[1] - x[1]) >= 200:
            cnt += 1
    
    return cnt


n = int(input())

lines = [input().split() for _ in range(n)]

pairs = [(x[0], int(x[1])) for x in lines]

pairs.sort(key=lambda tup: tup[1])

print('\n'.join(' '.join(str(item) for item in x) + ' ' +
    str(count(pairs, x)) for x in pairs)  + '\n')