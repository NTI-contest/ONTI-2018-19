inp = """4 4
rrrd
ldll
urru
rlrl
"""

import random

SEED = 6161
SUITE_SIZE = 20

random.seed(SEED)

def generate_one():
    m = random.randint(5, 20)
    n = random.randint(5, 20)
    field = "\n".join("".join(random.choice("uldr") for _ in range(n)) for _ in range(m))
    return "{} {}\n{}\n".format(m, n, field)

def generate():
    return [generate_one() for x in range(SUITE_SIZE)]

def solve(data):
    sizes, *lines = data.splitlines(False)
    m, n = map(int, sizes.split())
    vs = [[False for _ in range(n)] for _ in range(m)]
    x, y = 0, 0
    while True:
        if vs[y][x]:
            return("{} {}".format(y, x))
        vs[y][x] = True
        d = lines[y][x]
        if d == 'l':
            x, y = (x-1)%n, y
        elif d == 'r':
            x, y = (x+1)%n, y
        elif d == 'u':
            x, y = x, (y-1)%m
        elif d == 'd':
            x, y = x, (y+1)%m
        else:
            raise Exception("what?!")
        
def check(reply, clue):
    try:
        your = [int(x) for x in reply.split()]
        mine = [int(x) for x in clue.split()]
        return your == mine
    except Exception as e:
        return False, "ошибка формата"

def sanity(fn):
    tests = generate()
    ms = [solve(test) for test in tests]
    ys = [fn(test) for test in tests]
    flag = False
    for y, m, t in zip(ys, ms, tests):
        if not check(y, m):
            print("BAD TRY>>>\n{}\n>>>\nYOUR: {}\nMINE: {}".format(t, y, m))
            flag = True
    if flag:
        print("TEST FAILED :(")
    else:
        print("ALL RIGHT :D")

print(solve(sys.stdin.read()))