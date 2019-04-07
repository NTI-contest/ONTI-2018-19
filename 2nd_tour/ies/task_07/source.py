import random
import sys

random.seed(945591)

def genRow(count):
    row = [ 0 for _ in range(count) ]
    for i in range(count // 2):
        n = random.randint(0,count-1)
        if i != n:
            row[n] = random.random()
    total = sum(row)
    return [ x/total for x in row ]

def gen(count):
    affections = [ genRow(count) for _ in range(count) ]
    powers = [ -20 + 50*random.random() for _ in range(count) ]
    return powers, affections

class Power():
    influx = 0
    outflux = 0
    power = 0
    def __init__ ( self, power ):
        self.power = power

def makePower(rawValues):
    return [ Power(x) for x in rawValues ]

def balance(affections,pows):
    powers = pows.copy()
    for i in range(len(powers)):
        p = powers[i]
        if p.power > 0:
            p.outflux = p.power
            for j in range(len(powers)):
                q = powers[j]
                q.influx += affections[i][j] * p.outflux
    return powers

def missingPower(powers):
    return sum([ min(0,p.influx+p.power) for p in powers ])

def excessivePower(powers):
    return sum([ max(0,p.influx+p.power-p.outflux) for p in powers ])

def generate():
    num_tests = 20
    tests = []
    first = gen(10)
    tests.append((str(first)+'\n',first))
    for _ in range(num_tests-1):
        case = gen(random.randint(50,150))
        tests.append((str(case)+"\n",case))
    return tests

def solve(dataset):
    values,affections = eval(dataset)
    answer = missingPower(balance(affections,makePower(values)))
    return str(answer)

def check(reply,clue):
    ours = solve(str(clue))
    return abs(float(reply) - float(ours)) <= 1e10

print(solve(sys.stdin.read()))

