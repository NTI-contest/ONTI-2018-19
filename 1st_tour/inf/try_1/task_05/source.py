import sys

def solve():
    dataset = sys.stdin.read()
    n, a, b, c, d = map(int, dataset.split())
    ans = 0
    while n:
        ans += n
        n = n * a // b
    
    print(ans)
