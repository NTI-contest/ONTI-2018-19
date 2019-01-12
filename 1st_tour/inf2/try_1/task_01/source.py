n, m, k, h = [int(i) for i in input().split()]
print("Yes" if n - m * k > 0 and (n - m * k) % h == 0 else "No")
