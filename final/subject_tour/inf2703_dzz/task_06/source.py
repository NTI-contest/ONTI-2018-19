def get_square(picture, i, j, p, visited):
    
    nodes = [(i, j)]
    
    x = len(picture)
    y = len(picture[0])
    
    square = 0
    
    while nodes:
        i, j = nodes[0]
        nodes = nodes[1:]
        if i < 0 or i >= x or j < 0 or j >= y:
            continue
        if visited[i][j]:
            continue
        visited[i][j] = True
        square += 1
        
        if i > 0 and j > 0:
            if abs(picture[i][j] - picture[i - 1][j - 1]) < p:
                nodes.append((i - 1, j - 1))
        if i < x - 1 and j > 0:    
            if abs(picture[i][j] - picture[i + 1][j - 1]) < p:
                nodes.append((i + 1, j - 1))
        if i > 0 and j < y - 1:
            if abs(picture[i][j] - picture[i - 1][j + 1]) < p:
                nodes.append((i - 1, j + 1))
        if i < x - 1 and j < y - 1:
            if abs(picture[i][j] - picture[i + 1][j + 1]) < p:
                nodes.append((i + 1, j + 1))
        if i > 0:
            if abs(picture[i][j] - picture[i - 1][j]) < p:
                nodes.append((i - 1, j))       
        if i < x - 1:
            if abs(picture[i][j] - picture[i + 1][j]) < p:
                nodes.append((i + 1, j))
        if j > 0:
            if abs(picture[i][j] - picture[i][j - 1]) < p:
                nodes.append((i, j - 1))       
        if j < y - 1:
            if abs(picture[i][j] - picture[i][j + 1]) < p:
                nodes.append((i, j + 1))
                
    return square
        

def solve_test(x, y, p, picture):
    max_square = 0
    visited = [[False for _ in range(y)] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            if visited[i][j] == 0:
                cur_square = get_square(picture, i, j, p, visited)
                max_square = max(cur_square, max_square)
    
    return max_square
    
x, y, p = map(int, input().split())

d = [input() for _ in range(x)]

print(solve_test(x, y, p, [list(map(int, line.split())) for line in d]))