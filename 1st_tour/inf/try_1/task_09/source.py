import sys

def f(x, n, coeffs):
    res = 0
    for i in range(n + 1):
        res *= x
        res += coeffs[i]
    return res

def way(x0, step, n, coeffs):
    return math.sqrt(step ** 2 + (f(x0 + step, n, coeffs) - f(x0, n, coeffs)) ** 2)

def solve():
    dataset = sys.stdin.read()
    lst = dataset.split()
    
    n = int(lst[0])
    s = float(lst[-1])
    coeffs = list(map(int, lst[1:-1]))
    wayval = 0
    x = 0.0    
    step = 0.00001
    
    while(wayval < s):
        wayval += way(x, step, n, coeffs)
        x += step
    
    print(str(x))