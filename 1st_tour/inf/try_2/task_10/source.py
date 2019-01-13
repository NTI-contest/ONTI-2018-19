import sys

dataset = sys.stdin.read()

l = dataset.split()
n = int(l[0])
m = int(l[n + 1])
names = l[1: n + 1]
pairs = l[n + 2:]

matrix = [[1000 for _ in range(n)] for _ in range(n)]
for i in range(n):
    matrix[i][i] = 0
    
for i in range(m):
    a = names.index(pairs[2 * i])
    b = names.index(pairs[2 * i + 1])
    matrix[a][b] = 1
    matrix[b][a] = 1

for k in range(n):
    for i in range(n):
        for j in range(n):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

ans = 'Yes'
for i in range(n):
    for j in range(n):
        if matrix[i][j] > 6:
            ans = 'No'
            break

print(ans)