import sys
from itertools import accumulate

def solve():
    dataset = sys.stdin.read()
    lines = dataset.splitlines()
    
    values  = [int(v) for v in lines[1].split()]
    queries = [tuple(int(v) for v in query.split()) for query in lines[3:] if query.strip() != '']
    
    inbound  = [0] + list(accumulate(v if v > 0 else 0 for v in values))
    outbound = [0] + list(accumulate(v if v < 0 else 0 for v in values))
    
    answer = ''
    for l, r in queries:
        pos = inbound[r + 1] - inbound[l]
        neg = outbound[r + 1] - outbound[l]
        answer += '{} {}\n'.format(pos, -neg)
    
    print(answer)

