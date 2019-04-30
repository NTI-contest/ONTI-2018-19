from fractions import gcd

n, m = [int(i) for i in input().split()]
print(n // gcd(n, m))
