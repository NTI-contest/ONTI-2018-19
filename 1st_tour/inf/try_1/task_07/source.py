import sys

def is_in_line(x1, y1, x2, y2, x3, y3):
    return (x3 - x1) * (y2 - y1) == (y3 - y1) * (x2 - x1)

def solve():
    dataset = sys.stdin.read()
    x1, y1, x2, y2, x3, y3 = [int(x) for x in dataset.split()]
    if is_in_line(x1, y1, x2, y2, x3, y3):
        print("No")
    print("Yes")