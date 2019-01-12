import sys

def solve():
    dataset = sys.stdin.read()
    a, b, c = map(int, dataset.split())
    d = 0
    if b > c:
        for x in range(b):
            if (a * x) % b == c:
                d = x
                break
            
    return(d)