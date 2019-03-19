import sys

def get_med(q, n):
    ans = [0, 0, 0]
    size = n
        
    for i in range(3):
        pos = 0
        idx = 0
        val1 = (size - 1) // 2
        val2 = (size - 0) // 2
        #eprint(q[i])
        while (pos + q[i][idx] <= val1):
            #eprint(pos, val1, idx)
            pos += q[i][idx]
            idx += 1
        val1 = idx
        
        while (pos + q[i][idx] <= val2):
            pos += q[i][idx]
            idx += 1
        val2 = idx
        
        ans[i] = (val1 + val2) / 2
        
    return ans

dataset = sys.stdin.read()

d = dataset.split()
n = int(d[0])
numbers = list(map(int, d[1:]))

q = []

q.append([0] * 101)
q.append([0] * 101)
q.append([0] * 101)

sum1 = [0, 0, 0] 

for i in range(3 * n):
    q[i % 3][numbers[i]] += 1
    
sum1 = [sum([q[j][i] * i for i in range(101)]) for j in range(3)]
    
med = get_med(q, n)

for i in range(3):
    ten_p = n // 10
    idx = 0
    while (ten_p):
        x = min(q[i][idx], ten_p)
        ten_p -= x
        q[i][idx] -= x
        idx += 1
    
for i in range(3):
    ten_p = n // 10
    idx = 100
    while (ten_p):
        x = min(q[i][idx], ten_p)
        ten_p -= x
        q[i][idx] -= x
        idx -= 1   
    
sum2 = [sum([q[j][i] * i for i in range(101)]) for j in range(3)]

print(' '.join(str(x / n) for x in sum1))
print(' '.join(str(x) for x in med))
print(' '.join(str(x / (n - n // 10 - n // 10)) for x in sum2))
print(' '.join(str(x) for x in med))
