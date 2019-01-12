n = int(input())

s = input().strip()
s = s[::-1]

alphabet = 26
cost = list(map(int, input().split()))
bonus = list(map(int, input().split()))

ans = [0] * n
ans[0] = cost[ord(s[0]) - ord('a')]

st = [0] * n
ss = 1

for i in range(n - 1):
    l = -1
    r = ss - 1
    while l + 1 < r:
        mid = (l + r) // 2
        if st[mid] < i - bonus[ord(s[i + 1]) - ord('a')]:
            l = mid
        else:
            r = mid

    ans[i + 1] = ans[st[r]] + cost[ord(s[i + 1]) - ord('a')]

    while ss > 0 and ans[st[ss - 1]] >= ans[i + 1]:
        ss -= 1
    st[ss] = i + 1
    ss += 1

print(ans[n - 1])