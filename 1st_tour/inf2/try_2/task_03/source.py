n, k = (int(i) for i in input().split())
s = input()
print(len(set(s[i * k : (i + 1) * k] for i in range(n // k))))
