import random
import sys

SEED = 6161
NUM_CUBES = 6
SUITE_SIZE = 20
DESIRED_NUMBER = 21

random.seed(SEED)

def generate_cube():
    c = []
    for x in range(5):
        c.append(round(random.random() * 0.3 * (1 - sum(c)), 5))
    c.append(1-sum(c))
    random.shuffle(c)
    return c

def generate_one():
    cubes = "\n".join(" ".join("{:.5}".format(x) for x in generate_cube())
        for _ in range(NUM_CUBES))
    return cubes

def generate():
    return [generate_one() for x in range(SUITE_SIZE)]

def solve(data):
    cubes = [[float(x) for x in l.split()] for l in data.splitlines(False)]
    ans = 0
    
    def looper(acc, i, p):
        nonlocal ans
        if i == NUM_CUBES:
            return
        for x in range(1, 6 + 1):
            if acc + x == DESIRED_NUMBER and i == NUM_CUBES - 1:
                ans += p * cubes[i][x-1]
                return
            if acc + x > DESIRED_NUMBER:
                return
            looper(acc+x, i+1, p * cubes[i][x-1])

    looper(0, 0, 1)
    return str(ans)
        
def check(reply, clue):
    try:
        your = float(reply)
        mine = float(clue)
        return abs(your-mine) <= 0.00001
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