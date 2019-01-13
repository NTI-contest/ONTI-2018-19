import sys

dataset = sys.stdin.read()

n = int(dataset)
ans = 0

for _ in range(4):
    ans *= 256
    ans += n % 256
    n //= 256

print(ans)