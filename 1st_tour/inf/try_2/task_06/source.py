import sys

dataset = sys.stdin.read()

d = list(map(int, dataset.split()))
    
ans = 0
    
for i in range(1, d[0] * 2 + 2):
    ans = ans ^ d[i]

print(ans)