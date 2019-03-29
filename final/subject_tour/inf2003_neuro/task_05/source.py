from collections import defaultdict
from pprint import pprint

a, b = [int(v) for v in input().split()] # period of infectiousness
N = int(input().strip()) # number of appointments

met = defaultdict(lambda: defaultdict(set))
people = set()

for _ in range(N):
    D, M = [int(v) for v in input().split()] # day from day 0, member_qty
    Q = [int(v) for v in input().split()] # member ids
    for q in Q:
        met[D][q].update(v for v in Q if v != q)
    people.update(Q)

people = list(sorted(people))
last_appointment = max(met.keys())
t_max = last_appointment + b + 2

sick = [[-1] * (max(people) + 1) for _ in range(t_max)]
sick[0][0] = 0
infected = set([0])

for t in range(1, t_max):
    for p in people:
        if p in infected:
            continue 
        for dt in range(a, b + 1):
            for p_other in met[t][p]:
                if sick[t - dt][p_other] == 0:
                    sick[t][p] = 0
                    infected.add(p)

print(*sorted(infected))