import sys

def get_next(n, s):
    new_s = ''
    for i in range(n):
        for j in range(n):
            
            idx = [((i - 1), j - 1), \
                   ((i - 1), j), \
                   ((i - 1), j + 1), \
                   ((i), j - 1), \
                   ((i), j + 1), \
                   ((i + 1), j - 1), \
                   ((i + 1), j), \
                   ((i + 1), j + 1)] 
            
            idx = [x * n + y for (x, y) in idx if x >= 0 and x < n and y >= 0 and y < n]
            alive = sum([1 for x in idx if s[x] == '*'])
            if s[i * n + j] == 'x' and alive == 3:
                new_s += '*'
            elif s[i * n + j] == '*' and (alive == 2 or alive == 3):
                new_s += '*'
            else:
                new_s += 'x'
                
    return new_s    

def solve(dataset):
    dataset = sys.stdin.read()
    d = dataset.split()
    n = int(d[0])
    p = ''
    for x in d[1:]:
        p += x
    
    died = 'x' * n * n
    
    s = set([died])
    
    while True:
        if p in s:
            break
        else:
            s.add(p)
            p = get_next(n, p)
    
    ans = ''
    if p == died:
        ans += 'No\n'
    else:
        ans += 'Yes\n'
    ans += str(len(s) - 1) + '\n'
        
    print(ans)