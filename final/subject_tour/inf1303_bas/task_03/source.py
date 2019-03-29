n, m = (int(x) for x in input().split())
s = set(input().split())
for i in range(m):
    if input() in s:
        print('YES')
    else:
        print('NO')