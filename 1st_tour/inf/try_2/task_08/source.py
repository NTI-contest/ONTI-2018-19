import sys

def solve():
    dataset = sys.stdin.read()
    lst = list(map(int, dataset.split()))
    n = lst[0]
    lst = lst[1:]
    ans = [0] * (n + 1)
    ans[0] = 1
    
    for i in range(n):
        for j in range(i + 1, 0, -1):
            ans[j] -= ans[j - 1] * lst[i]
    
    if n % 2 == 0:
        ans = [-x for x in ans]
    
    print(' '.join(str(x) for x in ans))