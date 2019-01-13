import sys

dataset = sys.stdin.read()

n = int(dataset.split()[0])
    
d = {0:1}

for _ in range(11):
    tmp = {}
    for x in d.keys():
        for digit in range(10):
            if ((x + digit + 1) in tmp.keys()):
                tmp[x + digit + 1] += d[x]
            else:
                tmp[x + digit + 1] = d[x]
    d = tmp.copy()
    
if (n in d.keys()):
    ans = d[n]
else:
    ans = 0

print(ans)
