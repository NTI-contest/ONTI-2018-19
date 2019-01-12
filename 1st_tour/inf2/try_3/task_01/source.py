a, b, c, n = [int(x) for x in input().split()]
for i in sorted([a, b, c, a + b, a + c, b + c, a + b + c, 0], reverse=True):
    if i % n == 0:
        print(i // n)
        break