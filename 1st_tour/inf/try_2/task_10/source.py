import sys

def fire_clean(picture, i, j):
    visited = [[0 for _ in range(len(picture))] for _ in range(len(picture))]
    nodes = [(i, j)]
    
    while nodes:
        i, j = nodes[0]
        nodes = nodes[1:]
        if i < 0 or i >= len(picture) or j < 0 or j >= len(picture):
            continue
        if visited[i][j]:
            continue
        visited[i][j] = 1
        if picture[i][j] == 'x':
            picture[i][j] = '.'
            nodes += [
                (i - 1, j - 1),
                (i - 1, j), 
                (i - 1, j + 1), 
                (i, j - 1), 
                (i, j + 1), 
                (i + 1, j - 1), 
                (i + 1, j), 
                (i + 1, j + 1),
            ]      
    return
        

def solve_test(n, picture):
    groups = 0
    for i in range(n):
        for j in range(n):
            if picture[i][j] == 'x':
                groups += 1
                fire_clean(picture, i, j)           
    return str(groups) + ' '
    
    
def solve():
    dataset = sys.stdin.read()
    d = dataset.split()
    tn = int(d[0])
    idx = 1
    eprint(tn)
    ans = ''
    for _ in range(tn):
        ans += solve_test(int(d[idx]), [list(x) for x in d[idx + 1:idx + 1 + int(d[idx])]])
        
        idx += int(d[idx]) + 1
    print(ans)