from math import factorial


def binomial(n, m):
    return factorial(n) // factorial(m) // factorial(n - m)


n, m = map(int, input().split())
print(binomial(m - 1, n - 1) % (10 ** 9 + 7))
