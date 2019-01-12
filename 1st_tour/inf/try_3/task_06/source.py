import sys

def solve():
    dataset = sys.stdin.read()
    lines = dataset.splitlines()
    R, u, v = map(int, lines[0].split())
    n = int(lines[1])
    
    points = []
    
    for l in lines[2 : 2 + n]:
        tmp = list(map(int, l.split()))
        points.append((tmp[0], tmp[1]))
        
    p = list(map(int, lines[-1].split()))
    
    s = 0
    
    for ant in points:
        R2_ant = sum([(ant[i] - p[i]) ** 2 for i in range(2)])
        if 4 * R2_ant <= R * R:
            s += u
        elif R2_ant <= R * R:
            s += v
            
    print(int(s))