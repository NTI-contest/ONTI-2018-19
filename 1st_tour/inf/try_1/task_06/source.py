import sys

def solve(dataset):
    dataset = sys.stdin.read()
    input = dataset.split()
    n = int(input[0])
    m = int(input[1])
    matrix = [[int(input[2 + x * m + y]) for y in range(m)] for x in range(n)]
    
    for i in range(n):
        for j in range(m):
            list = []
            if i > 0:
                list.append(matrix[i - 1][j])
            if j > 0:
                list.append(matrix[i][j - 1])
            if list:
                matrix[i][j] = min(matrix[i][j], max(list))
    
    print(matrix[n - 1][m - 1])