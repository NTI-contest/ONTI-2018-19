s = input().strip()
n = len(s)
for i in range((n - 1) // 2 + 1):
    if s[i] != s[n - 1 - i] or i == (n - 1) // 2:
        t = "".join([('' if n - 1 - i == j else s[j]) for j in range(n)])
        s = "".join([('' if i == j else s[j]) for j in range(n)])
        break
print('YES' if t == t[::-1] or s == s[::-1] else 'NO')
