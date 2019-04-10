from math import ceil, sqrt

def arrows(h):
    global D, K
    sd = sqrt((2*D - K)**2 + 8*K*h)
    x1, x2 = int((K - 2*D - sd)/2/K), int(ceil((K - 2*D + sd)/2/K))
    return x1 if x1 > 0 else x2

N, D, K, *H = map(int, open('input.txt', 'r').read().split())
open('output.txt', 'w').write(str(sum(map(arrows, H))))
