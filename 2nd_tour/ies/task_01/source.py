import random
import copy
import itertools
import sys

totalPlayers = 5
totalFlowers = 3
totalPoints = 50
allP = [ x for x in range(totalPlayers)]
allF = [ x for x in range(totalFlowers)]
allPr = [ x for x in range(totalPoints)]

leftLim = -2
rightLim = 2

def patchLim(r):
    return r*(rightLim-leftLim) + leftLim

random.seed(883)

def smoothgen():
    num2 = []
    for _ in allPr:
        num2.append(patchLim(random.random()))
    num1 = [0]
    for i in range(totalPoints-1):
        new = num1[i] + num2[i]
        num1.append(new)
    num0 = [0]
    for i in range(totalPoints-1):
        new = num0[i] + num1[i]
        num0.append(new)
    adjustSign = min(num0)
    for i in range(totalPoints):
        num0[i] = num0[i]-adjustSign
    adjustScale = sum(num0)
    for i in range(totalPoints):
        num0[i] = num0[i]/adjustScale
    return num0

def genDistro():
    byPlayers = []
    for i in allP:
        byFlowers = []
        for j in allF:
            byFlowers.append(smoothgen())
        byPlayers.append(byFlowers)
    return byPlayers

distro = genDistro()

def d(player,flower,price):
    return distro[player][flower][price]

def probLessThanValue(value,player,flower):
    result = 0
    for i in range(value):
        result += d(player,flower,i)
    return result

def probOutcomeSucc(parts,plrs,flower,price,winner):
    result = 1
    for p in parts:
        if p == winner:
            result *= d(p,flower,price) / len(plrs)
        elif p in plrs:
            result *= d(p,flower,price)
        else:
            result *= probLessThanValue(price,p,flower)
    return result

def powerset(parts):
    result = [[]]
    for p in parts:
        new = []
        cp = copy.deepcopy(result)
        for x in cp:
            x.append(p)
            new.append(x)
        result += new
    return result

def outcomes(participants,who):
    parts = copy.deepcopy(participants)
    if who in parts:
        parts.remove(who)
        outs = powerset(parts)
        for o in outs:
            o.append(who)
        return outs
    else:
        return []

def mainFn(parts,winner,price,flower):
    if winner in parts:
        outs = outcomes(parts,winner)
        result = 0
        for o in outs:
            result += probOutcomeSucc(parts,o,flower,price,winner)
        return result
    else:
        return 0

def probPlayer(others,flower,who):
    result = 0
    for pr in allPr:
        result += mainFn(others,who,pr,flower)
    return result

def processChain(participants,flowers):
    if flowers == []:
        return 0
    else:
        result = 0
        f,*fs = flowers
        for w in participants:
            expect = 0
            for pr in allPr:
                expect += pr * mainFn(participants,w,pr,f)
            parts = copy.deepcopy(participants)
            parts.remove(w)
            result += expect + probPlayer(participants,f,w) * processChain(parts,fs)
    return result

def var(fs):
    return processChain(allP,fs)

def answer():
    fs = itertools.permutations(allF)
    exemplar = var(allF)
    best = 0
    for f in fs:
        v = var(f)
        if best < v:
            best = v
    result = (best-exemplar)/exemplar*100
    return result

def solu(values):
    global distro
    oldDistro = copy.deepcopy(distro)
    distro = values
    result = answer()
    distro = oldDistro
    return result

def testD():
    global distro
    oldDistro = copy.deepcopy(distro)
    distro = testDistMap2
    val = d(1,1,50)
    result = val == 8.283601731573895e-3
    if not result:
        print(val)
    distro = oldDistro
    return result

def testLessThan():
    global distro
    oldDistro = copy.deepcopy(distro)
    distro = testDistMap2
    val = probLessThanValue(50,0,0)
    result =  (val == 0.7391552524635776)
    if not result:
        print(val)
    distro = oldDistro
    return result

def testOutcomeSucc():
    global distro
    oldDistro = copy.deepcopy(distro)
    distro = testDistMap2
    val = probOutcomeSucc(allP,[1,2],0,50,1)
    result = val == 5.269109353831852e-7
    if not result:
        print(val)
    distro = oldDistro
    return result

def testResult():
    global distro
    oldDistro = copy.deepcopy(distro)
    distro = testDistMap2
    val = answer()
    result = val == 8.9573356038474e-2
    if not result:
        print(val)
    distro = oldDistro
    return result

def test():
    print("testD",testD())
    print("testLessThan",testLessThan())
    print("testOutcomeSucc",testOutcomeSucc())
    print("testResult",testResult())

def generate():
    return [ str(genDistro())+"\n" for _ in range(10) ]

def solve(dataset):
    return str(solu(eval(dataset)))

def check(reply,clue):
    their = eval(reply)
    our = eval(clue)
    if abs(our-their) < 1e-10:
        return True
    if our > their:
        feedback = "Слишком мало, можно лучше!"
    if our < their:
        feedback = "Слишком много!"
    if their < 0:
        feedback = "Как минимум ноль!"
    return False, feedback

def testStepik():
    tests = generate()
    for raw in tests:
        sol = solve(raw)
        print(check(sol,solve(raw)))


print(solve(sys.stdin.read()))