import random
import sys

patternS = [0.0,0.0,0.0,0.0,0.0,0.0,1.3,2.75,3.95,5.5,7.5,9.5,11.5,13.5,14.65,15.0,
15.0,13.55,10.75,9.4,7.5,5.5,3.15,0.8]
patternC = [2.05,1.2000000000000002,1.0499999999999998,1.1,1.35,1.55,
1.7000000000000002,2.0,2.3,2.8,3.1500000000000004,2.85,2.05,1.9,1.7000000000000002,
2.05,2.55,3.25,4.15,4.95,6.4,6.3,4.699999999999999,3.45]

random.seed(8457)

cost = 10

def gen():
    sun = []
    house = []
    for _ in range(30):
        sun += [ x * ( 0.8 + 0.4 * random.random()) for x in patternS ]
        house += [ x / 3 * ( 0.8 + 0.4 * random.random()) for x in patternC ]
    return sun, house

def scale(intensity):
    return intensity / 10 * 1.5

def hourEconomy(sun,cons):
    power = scale(sun)
    return cost * min(power,cons)

def ans(suns,houses):
    #print(sum([h * cost for h in houses]))
    q = list(zip(suns,houses))
    economies = [ hourEconomy(s,c) for s,c in q ]
    return sum(economies)

#ss,cc = gen()
#print(ans(ss,cc))

def generate():
    result = []
    for _ in range (20):
        test = gen()
        result.append((str(test),test))
    return result

def solve(dataset):
    suns,houses = eval(dataset)
    return str(ans(suns,houses))

def check(reply,clue):
    their = eval(reply)
    s,h = clue
    our = ans(s,h)
    return abs(our-their) <= 1

print(solve(sys.stdin.read()))