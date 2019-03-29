from math import sqrt

N, k, b, S = [int(v) for v in input().split()]

d_sum = 0.0
outliers_qty = 0

for _ in range(N):
    x, y = [int(v) for v in input().split()]
    d = abs((b + k * x - y) / sqrt(1.0 + k * k))
    d_sum += d
    if d > S:
        outliers_qty += 1

print('{:.6f} {:.6f}'.format(d_sum / N, outliers_qty / N))
