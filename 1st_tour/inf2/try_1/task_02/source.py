def solve():
    n = int(input())
    s = [int(i) for i in input().split()]

    ok = True
    sum = 0
    for i in range(n):
        ai = sorted([int(i) for i in input().split()])
        for j in range(s[i]):
            ok &= (ai[j] == sum + j + 1)
        sum += s[i]

    return "Yes" if ok else "No"


t = int(input())

for i in range(t):
    print(solve())
