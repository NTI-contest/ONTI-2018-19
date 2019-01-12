import sys

def solve():
    dataset = sys.stdin.read()
    x = int(dataset) 
    a = 6
    b = 3
    c = 8
    d = 7
    return print((a * x * x + b * x + c) % d)