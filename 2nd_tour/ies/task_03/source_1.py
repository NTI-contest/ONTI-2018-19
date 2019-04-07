import random
import copy
import sys

random.seed(796)

def genLow():
    result=[]
    for _ in range(4):
        a = round(100*random.random())
        b = round(100*random.random())
        result.append((a,b))
    return result

def genHigh():
    result=[]
    for _ in range(4):
        a = random.randrange(8)
        b = random.randrange(8)
        result.append((a,b))
    return result

def genLG():
    return game(genLow())

def genHG():
    return game(genHigh())

def genTourStr():
    l = genLow()
    h1 = genHigh()
    h2 = genHigh()
    h3 = genHigh()
    h4 = genHigh()
    return [h4,h3,h2,h1,l]

class game:
    aa = 0
    ab = 0
    ba = 0
    bb = 0
    def __init__(self,values):
        self.aa = values[0]
        self.ab = values[1]
        self.ba = values[2]
        self.bb = values[3]

zeroGame = game([(0,0),(0,0),(0,0),(0,0)])

class tour:
    highs = []
    lows = copy.deepcopy(zeroGame)
    def __init__(self,values):
        self.highs = []
        self.lows = copy.deepcopy(zeroGame)
        self.lows = values[0]
        for v in (values[1:]):
            self.highs.append(v)

def prettyTour(tour):
    print("TOURNAMENT")
    for x in range(len(tour.highs)):
        print("tour",x)
        prettyGame(tour.highs[x])
    print("low-level")
    prettyGame(tour.lows)

dummyLowGame = game([(61,90),(3,87),(97,14),(76,29)])

def prettyGame(g):
    print("AA",g.aa)
    print("AB",g.ab)
    print("BA",g.ba)
    print("BB",g.bb)

def flip(x):
    a,b = x
    return (b,a)

def flipGame(source):
    result = copy.deepcopy(zeroGame)
    result.aa = flip(source.aa)
    result.ab = flip(source.ba)
    result.ba = flip(source.ab)
    result.bb = flip(source.bb)
    return result

def scoreGame(game,s1,s2):
    if s1 and s2:
        return game.aa
    if s1 and (not s2):
        return game.ab
    if (not s1) and s2:
        return game.ba
    if (not s1) and (not s2):
        return game.bb

strDummyTour = str(
    [ [(2,1),(5,0),(4,2),(0,5)]
    , [(5,4),(3,0),(2,5),(3,5)]
    , [(6,0),(2,2),(2,0),(7,5)]
    , [(2,7),(6,0),(6,1),(1,2)]
    , [(61,90),(3,87),(97,14),(76,29)]
    ])
def fromStrTour(t):
    values = eval(t)
    #print("LEN1",len(values))
    games = [ game(v) for v in reversed(values) ]
    #print("LEN2",len(games))
    #for g in games:
        #print("####")
        #prettyGame(g)
        #print("####")
    result = tour(games)
    #print("LEN3",len(result.highs))
    return tour(games)

#dummyHighGame1 = Game {aa = (Eye,Rematch), ab = (Eye2,AllA), ba = (Eye2,AllB), bb = (AllB,Eye)}
dummyHighGame1 = game([(2,7),(6,0),(6,1),(1,2)])
#dummyHighGame2 = Game {aa = (Eye2,AllA),       ab = (Eye,Eye),       ba = (Eye,AllA),     bb = (Rematch,Generous)}
dummyHighGame2 = game([(6,0),(2,2),(2,0),(7,5)])
#dummyHighGame3 = Game {aa = (Generous,Greedy), ab = (MinMax,AllA),   ba = (Eye,Generous), bb = (MinMax,Generous)}
dummyHighGame3 = game([(5,4),(3,0),(2,5),(3,5)])
#dummyHighGame4 = Game {aa = (Eye,AllB),        ab = (Generous,AllA), ba = (Greedy,Eye),   bb = (AllA,Generous)}
dummyHighGame4 = game([(2,1),(5,0),(4,2),(0,5)])
dummyTour = tour([dummyLowGame,dummyHighGame1,dummyHighGame2,dummyHighGame3,dummyHighGame4])

def choice(strat,game,history):
    if strat == 0: #All A
        return True
    if strat == 1: #All B
        return False
    if strat == 2: #Eye for eye
        if len(history) == 0:
            return True
        else:
            return history[-1]
    if strat == 3: #MinMax, most guaranteed
        worstA = min(game.aa[0],game.ab[0])
        worstB = min(game.ba[0],game.bb[0])
        return worstA >= worstB
    if strat == 4: #Greedy, max possible
        bestA = max(game.aa[0],game.ab[0])
        bestB = max(game.ba[0],game.bb[0])
        return bestA >= bestB
    if strat == 5: #Generous, max possible for opponent
        bestA = max(game.aa[1],game.ab[1])
        bestB = max(game.ba[1],game.bb[1])
        return bestA >= bestB
    if strat == 6: #Eye for two eyes
        if len(history) < 2:
            return True
        else:
            return history[-1] or history[-2]
    if strat == 7: #Rematch, maximum for last round
        if len(history) == 0:
            return choice(3,game,history)
        else:
            if history[-1]:
                return game.aa[0] >= game.ba[0]
            else:
                return game.ab[0] >= game.bb[0]

def simpleGame(game,s1,s2):
    history1 = []
    history2 = []
    score1 = 0
    score2 = 0
    game1 = game
    game2 = flipGame(game)
    for _ in range(20):
        c1 = choice(s1,game1,history2)
        c2 = choice(s2,game2,history1)
        sc1,sc2 = scoreGame(game1,c1,c2)
        history1.append(c1)
        history2.append(c2)
        score1 += sc1
        score2 += sc2
    return(score1,score2)

def foldGame(gameH,gameL):
    result = copy.deepcopy(zeroGame)
    result.aa = simpleGame(gameL,gameH.aa[0],gameH.aa[1])
    result.ab = simpleGame(gameL,gameH.ab[0],gameH.ab[1])
    result.ba = simpleGame(gameL,gameH.ba[0],gameH.ba[1])
    result.bb = simpleGame(gameL,gameH.bb[0],gameH.bb[1])
    return result

def playTournament(t,s1,s2):
    tour = copy.deepcopy(t)
    effective = copy.deepcopy(tour.lows)
    #prettyGame(effective)
    for g in tour.highs:
        #print("LEN",len(tour.highs))
        effective = foldGame(g,effective)
        #print("folding…")
        #prettyGame(effective)
    return simpleGame(effective,s1,s2)

def fullTournament(tour,s):
    t = copy.deepcopy(tour)
    result1 = 0
    result2 = 0
    for o in range(8):
        result1 += playTournament(t,s,o)[0]
    #print(1,result1)
    for o in range(8):
        result2 += playTournament(t,o,s)[1]
    #print(2,result2)
    return result1 + result2

def ans(tour):
    t = copy.deepcopy(tour)
    result = 0
    best = 0
    for x in range(8):
        que = fullTournament(t,x)
        #print("QUE",x,que)
        if que > best:
            best = que
            result = 1
        elif que == best:
            result += 1
    #print("-----",best)
    return result

def test():
    g = dummyLowGame
    print(simpleGame(g,2,7))
    print("~~~~~~~~~~")
    print(scoreGame(g,True,True))
    print("~~~~~~~~~~")
    prettyGame(flipGame(dummyLowGame))
    print("~~~~~~~~~~")
    prettyGame(foldGame(dummyHighGame1,dummyLowGame))
    print("FF",simpleGame(foldGame(dummyHighGame4,dummyLowGame),3,0))
    print("-")
    prettyGame(foldGame(dummyHighGame2,dummyLowGame))
    print("-")
    prettyGame(foldGame(dummyHighGame3,dummyLowGame))
    print("-")
    prettyGame(foldGame(dummyHighGame4,dummyLowGame))
    #print("~~~~~~~~~~")
    #prettyTour(dummyTour)
    print("~~~~~~~~~~")
    test4_2=foldGame(dummyHighGame3,foldGame(dummyHighGame4,dummyLowGame))
    prettyGame(test4_2)
    print("~~~~~~~~~~")
    for x in range(8):
        for y in range(8):
            print(x,y,playTournament(dummyTour,x,y))
    print("~~~~~~~~~~")
    print(fullTournament(dummyTour,2))
    #prettyTour(flipTournament(dummyTour))
    print(ans(dummyTour))
    print(ans(fromStrTour(strDummyTour)))
    for x in generate():
        print(ans(fromStrTour(x)))

def generate():
    return [ str(genTourStr()) for _ in range(30) ]

def solve(dataset):
    return str(ans(fromStrTour(dataset)))

def check(reply,clue):
    their = eval(reply)
    ours = eval(clue)
    if their == ours:
        return True
    else:
        return False


print(solve(sys.stdin.read()))