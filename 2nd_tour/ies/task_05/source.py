import random
import sys

content = [ 1.5935004
    , 1.0997878
    , 0.5595438
    , 0.3955478
    , 0.488944
    , 0.6068851
    , 0.62520367
    , 0.7163142
    , 0.78384954
    , 0.69044185
    , 0.82434213
    , 1.1544989
    , 1.193051
    , 1.0579418
    , 0.9862855
    , 1.2018712
    , 1.2106589
    , 1.5743363
    , 1.9298786
    , 2.4665824
    , 2.7173998
    , 2.3626094
    , 1.7456802
    , 1.5448046
    ]

random.seed(45235)
#random.seed(None)

def gen():
    constant = []
    variable = []
    for x in content:
        r1 = random.random() * 0.2 + 0.65
        r2 = random.random() * 0.2 + 0.05
        constant.append(x*r1)
        variable.append(x*r2)
    return constant, variable

defLower = 300
defUpper = 600
clause1Threshold = (500/365)
clause3Threshold = (1000/365)
powerProfit = (40000/365)
searchDepth = 2.5 # Ищем тарифы от 0 до 2.5 x текущий

def shifter(constant,variable,s):
    shifted = []
    for i in range(len(constant)):
        shifted.append(constant[i] + variable[(i+s)%24])
    return shifted

def hourLow(x):
    h = x % 24
    return (h<6) or (h>22) or ((h>11) and (h<16))

def cacheShifts(constant,variable):
    result = []
    for h in range(24):
        lower = 0
        higher = 0
        hourly = shifter(constant,variable,h)
        for hh in range (0,24):
            if hourLow(hh):
                lower += hourly[hh]
            else:
                higher += hourly[hh]
        result.append((lower,higher))
    return result

def cachePeaks(constant,variable):
    result = []
    for sh in range(24):
        best = 0
        values = shifter(constant,variable,sh)
        for v in values:
            if v > best:
                best = v
        result.append(best)
    return result

constant,variable = gen()

#cached = cacheShifts(constant,variable)
#cachedPeaks = cachePeaks(constant,variable)

def costsOnShift(cached,lower,upper,sh):
    low,up = cached[sh]
    return (low*lower + up*upper)

def currentDaily(cached):
    return costsOnShift(cached,defLower,defUpper,0)
#print(currentDaily)

def clause1(cached,lower,upper):
    old = currentDaily(cached)
    new = old
    for i in range(24):
        que = costsOnShift(cached,lower,upper,i)
        if que < new:
            new = que
    return old >= new + clause1Threshold

#def peak(sh):
    #return cachedPeaks[sh]

def profits(cached,cachedPeaks,lower,upper,sh):
    profitFromPower = ((cachedPeaks[0] - cachedPeaks[sh]) * powerProfit )
    profitFromPay = costsOnShift(cached,lower,upper,sh) - currentDaily(cached)
    #print(lower,upper,sh,profitFromPower,profitFromPay)
    return profitFromPay + profitFromPower

def sureProfits(cached,cachedPeaks,lower,upper):
    if ( lower == defLower and upper == defUpper ):
        return 0
    result = 0
    worstProfit = 1000000000
    for i in userAcceptableShifts(cached,lower,upper):
        pr = profits(cached,cachedPeaks,lower,upper,i)
        if pr < worstProfit:
            result = pr
    return result

def clause3(cached,lower,upper):
    old = currentDaily(cached)
    new = costsOnShift(cached,lower,upper,0)
    return new > old + clause3Threshold

def userAcceptableShifts(cached,lower,upper):
    result = []
    for i in range(24):
        if costsOnShift(cached,lower,upper,i) + clause1Threshold <= currentDaily(cached):
            result.append(i)
    return result

def clause2(cached,cachedPeaks,lower,upper):
    result = profits(cached,cachedPeaks,lower,upper,0) > 0
    for i in userAcceptableShifts(cached,lower,upper):
        result = result and profits(cached,cachedPeaks,lower,upper,i) > 0
    return result

def evaluateTariffs(cached,cachedPeaks,lower,upper):
    return clause1(cached,lower,upper) and clause2(cached,cachedPeaks,lower,upper) and clause3(cached,lower,upper)

def findTariffs(cached,cachedPeaks):
    result = []
    for lower in range(0,defLower):
        for upper in range (defUpper,defUpper * 3):
            if evaluateTariffs(cached,cachedPeaks,lower,upper):
                result.append((lower,upper))
    return result

def best(cached,cachedPeaks):
    result = (defLower,defUpper,0)
    bestProfit = 0
    for (l,u) in findTariffs(cached,cachedPeaks):
        pr = sureProfits(cached,cachedPeaks,l,u)
        if pr > bestProfit:
            bestProfit=pr
            result=(l,u,bestProfit)
    return result

def generate():
    tests = []
    for _ in range(20):
        q = gen()
        tests.append((str(q)+"\n",q))
    return tests

def solve(dataset):
    constant,variable = eval(dataset)
    cached = cacheShifts(constant,variable)
    cachedPeaks = cachePeaks(constant,variable)
    lower,upper,value = best(cached,cachedPeaks)
    #print(lower, upper, value)
    return str((lower,upper))

def check(reply,clue):
    theirLow, theirUpper = eval(reply)
    constant,variable = clue
    cached = cacheShifts(constant,variable)
    cachedPeaks = cachePeaks(constant,variable)
    _,_,ourValue = best(cached,cachedPeaks)
    theirValue = sureProfits(cached,cachedPeaks,theirLow,theirUpper)
    return abs(theirValue - ourValue) <= 3

def test():
    g = generate()
    for i in range(len(g)):
        print(g[i][0])
        print(solve(g[i][0]))

print(solve(sys.stdin.read()))