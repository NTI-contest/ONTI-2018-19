import sys
import string

def solve():
    dataset = sys.stdin.read()
    s = set([])

    for x in dataset:
        if x not in string.ascii_letters:
            s.add(x)
            
    t = dataset
    for x in t:
        for l in s:
            t = t.replace(l, ' ')
    
    t = t.lower()
    t = t.split()       
    
    d = {}

    for x in t:
        if x in d.keys():
            d[x] += 1
        else:
            d[x] = 1

    sorted_d = sorted(d.items(), key=lambda x: x[0], reverse=False)
    sorted_d.sort(key=lambda x: x[1], reverse=True)

    tmp = ''

    for x in sorted_d:
        tmp += '{} {}\n'.format(x[0], x[1])
    
    print(tmp)