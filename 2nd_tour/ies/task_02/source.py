import random
import copy
import sys

sample = [91.05173216589283, 346.59744306410516, 79.340611380049, 6.301441137920902, 34.63321051774173, 283.7442062865518, 462.85639563921933, 18.35969426088177, 114.42284118915013, 348.2511151684352, 35.81719885313268, 49.63674917703884, 467.9423981733799, 238.65743487391796, 147.2073340259839, 312.48489408473336, 138.01039332211423, 355.1005034359866, 29.340271106787984, 99.15946433242176, 101.62375687795341, 141.7968745962582, 264.1127225211994, 390.7520075028461, 26.574805514157045, 403.57290262223626, 303.2238232129529, 26.84536690537845, 50.625385690392626, 352.5875266607501, 490.5712855832286, 416.65057322723743, 122.00634222950978, 335.9327639665609, 284.63060901729824, 160.79226719983157, 223.84570254433135, 413.4381031366249, 187.54717290087862, 128.90402815207682, 159.9803378175234, 14.171716784140491, 155.82255763644835, 304.81212895990535, 45.49900226772919, 102.1328582020983, 279.3144857150673, 17.220775870782532, 11.775763243956991, 420.3908810294901, 218.56532462565573, 114.08772495108836, 474.84396820456203, 23.42964393526904, 488.342275079058, 140.96501499579327, 298.9578766530911, 267.67125182920097, 354.611490764674, 226.22210041061237, 62.486648272655984, 165.4886048470618, 374.29038006374896, 451.369147364035, 77.13392481127703, 151.34737510649012, 32.727027013870156, 295.5116227866447, 226.4690930528016, 424.58867910418365, 69.47863785878867, 234.0665621852868, 378.7013351244484, 443.67743755922623, 431.7846439734082, 363.81894140612695, 440.6357464469665, 453.521156833, 494.61361579067295, 354.0936576752547, 403.9161844666748, 147.84681444651815, 411.5024834919147, 64.96641657683537, 435.45151943325885, 374.9547328567214, 418.8032864136387, 463.61590561438766, 474.47404786220955, 264.00569373194526, 72.32714571028217, 225.68351098136608, 494.647162066111, 294.1248402828908, 339.89532040440764, 91.82306688959734, 254.15497797507396, 19.47245737881847, 392.5312375132503, 23.220173991813397]

def timeme(fn):
    from time import time
    def inner(*args, **kwargs):
        start = time()    
        r = fn(*args, **kwargs)
        end = time()
        print(fn.__name__, end-start)
        return r
    return inner

def testStepikOne(fn):
    test = generate()[0]
    your = timeme(fn)(test)
    print("your", your)
    clue = timeme(solve)(test)
    print("mine", clue)
    print(check(your,clue))
users = 100
userCount = -1

choiceSmallSolar = 0
choiceHugeSolar = 1
choiceBadInv = 2
choiceGoodInv = 3
choiceNone = 4

def traceChoice(c):
    if c == 0:
        return("Small")
    if c == 1:
        return("Huge")
    if c == 2:
        return("Bad")
    if c == 3:
        return("Good")
    if c == 4:
        return("None")

random.seed(532)

def patchRandom(r):
    highest = 500
    lowest = 5
    return r*(highest-lowest)+lowest

def sampleGen():
    result = []
    for v in sample:
        result.append(User(v))
    return result

def genPowers():
    result=[]
    for _ in range(users):
        result.append(patchRandom(random.random()))
    return result

def makeUsers(powers):
    result = []
    for p in powers:
        result.append(User(p))
    return result

def gen():
    result = []
    for _ in range(users):
        result.append(User(patchRandom(random.random())))
    return result

class User():
    consumption = 0
    generation = 0
    bandwidthGood = 0
    bandwidthBad = 0
    uid = 0
    def __init__(self,c):
        global userCount
        self.uid = userCount
        userCount += 1
        self.consumption = c
    def show(self):
        print("Cons",self.consumption,"Gen",self.generation,"Good",self.bandwidthGood,"Bad",self.bandwidthBad)
    def powerNeed(self):
        return max(0,self.consumption-self.generation)
    def sellingPower(self):
        fullBW = self.bandwidthBad + self.bandwidthGood
        fullG = self.generation - self.consumption
        if fullG <= 0:
            return 0
        else:
            return min(fullBW,fullG)
    def freeBandwidth(self):
        fullBW = self.bandwidthBad + self.bandwidthGood
        fullG = self.generation - self.consumption
        if fullG <= 0:
            return fullBW
        else:
            return max(0,fullBW - fullG)

def price(month,choice):
    if choice == choiceSmallSolar:
        pr = 10000
    elif choice == choiceHugeSolar:
        pr = 25000
    elif choice == choiceBadInv:
        pr = 15000
    elif choice == choiceGoodInv:
        pr = 20000
    else:
        pr = 0
    return pr #* 0.97 ** ( month // 12 )

def power(choice):
    if choice == choiceSmallSolar:
        return 2
    if choice == choiceHugeSolar:
        return 6
    if choice == choiceBadInv:
        return 5
    if choice == choiceGoodInv:
        return 5
    else:
        return 0

def payoffs(month,user,marketPrice,choice):
    if choice == choiceSmallSolar or choice == choiceHugeSolar:
        if user.powerNeed() >= power(choice):
            pwr = power(choice)
        elif user.powerNeed() <= 0:
            pwr = min(user.freeBandwidth(),power(choice))/2
        else:
            pwr = user.powerNeed() + min(user.freeBandwidth(),power(choice)-user.powerNeed())/2
        if pwr == 0:
            return float("inf")
        return price(month,choice)/pwr/marketPrice
    elif choice == choiceNone:
        return float("inf")
    elif choice == choiceBadInv or choice == choiceGoodInv:
        if user.powerNeed() > 0 or user.freeBandwidth() > 0:
            return float("inf")
        else:
            return price(month,choice) \
                / ( marketPrice / 2 ) \
                / min( power(choice),
                       user.generation-user.consumption-user.bandwidthBad-user.bandwidthGood)

threshold = 24 * 365 * 3

def userChoice(month,user,marketPrice,canBuyBad):
    if canBuyBad:
        opts = [ choiceSmallSolar, choiceHugeSolar, choiceBadInv, choiceGoodInv ]
    else:
        opts = [ choiceSmallSolar, choiceHugeSolar, choiceGoodInv ]
    best = choiceNone
    bestPayoff = float("inf")
    for o in opts:
        newPayoff = payoffs(month,user,marketPrice,o)
        if newPayoff < bestPayoff:
            best = o
            bestPayoff = newPayoff
    if payoffs(month,user,marketPrice,best) < threshold:
        return best
    return choiceNone

def isSystemBroken(users):
    cons = 0
    badPower = 0
    goodPower = 0
    for u in users:
        badPower += u.bandwidthBad
        goodPower += u.bandwidthGood
        cons += u.powerNeed()
        #print(u.uid,u.consumption,u.generation,u.powerNeed())
    result = badPower / cons >= 0.3
    #print("Bad_power_and_cons_and_good_power",result,badPower/cons,badPower,cons,goodPower)
    return result
    #return badPower / cons >= 0.3 #max(cons,badPower+goodPower) >= 0.3

def applyChoice(user,choice):
    #traceChoice(choice)
    if choice == choiceSmallSolar or choice == choiceHugeSolar:
        user.generation += power(choice)
    elif choice == choiceBadInv:
        user.bandwidthBad += power(choice)
    elif choice == choiceGoodInv:
        user.bandwidthGood += power(choice)

def canAddBad(users):
    cons = 0
    badPower = power(choiceBadInv)
    for u in users:
        badPower += u.bandwidthBad
        cons += u.powerNeed()
    result = False
    if cons > 0:
        result = badPower / cons < 0.1
    #print(result, badPower / cons)
    return result

def fold(marketPrice,month,users):
    for u in users:
        oldUser = copy.deepcopy(u)
        applyChoice(u,userChoice(month,oldUser,marketPrice,canAddBad(users)))
        #u = applyChoice(oldUser,userChoice(month,oldUser,marketPrice,canAddBad(users)))

def fixedPrice(users):
    c = 1.5
    operationalCosts = 1e6 * 12 / 365 / 24
    userPower = 0
    cons = 0
    for u in users:
        userPower += u.sellingPower()
        cons += u.powerNeed()
    soldPower = cons - userPower
    if soldPower <= 0:
        return float("inf")
    return ( c + operationalCosts / soldPower ) * 1.05

def run(users):
    month = 0
    fixed = fixedPrice(users)
    marketPr = fixedPrice(users)
    while True:
        if isSystemBroken(users):
            #return users
            return month
        if month % 12 == 0:
            fixed = fixedPrice(users)
        marketPr = fixed
        fold(marketPr,month,users)
        if month == 7:
            #print(marketPr)
            for u in users:
                if u.bandwidthBad > 0:
                    pass#u.show()
        month += 1
    #return(users)
    return(month)

def test():
    dummyPrice = 2
    dummy = User(19.47245737881847)
    dummy.generation = 20.2
    dummy.bandwidthBad = 0
    dummy.bandwidthGood = 0
    #print(dummy.powerNeed())
    print(payoffs(1,dummy,dummyPrice,0))
    print(payoffs(1,dummy,dummyPrice,1))
    print(payoffs(1,dummy,dummyPrice,2))
    print(payoffs(1,dummy,dummyPrice,3))
    print("fs",traceChoice(userChoice(1,dummy,dummyPrice,False)))
    print("tr",traceChoice(userChoice(1,dummy,dummyPrice,True)))
    users = sampleGen()
    #users = gen()
    #for u in users:
        #print(u.uid,u.consumption)
    #stopped = run(users)
    #for s in stopped:
        #print(s.uid,s.consumption,s.generation,s.bandwidthGood,s.bandwidthBad)
    #print("Result:",run (users))
    #print(newMarketPrice(3,[dummy]))

def generate():
    return [ str(genPowers())+"\n" for _ in range(20) ]

def solve(dataset):
    return str(run(makeUsers(eval(dataset))))

def check(reply,clue):
    their = eval(reply.strip())
    our = eval(clue.strip())
    return our == their


print(solve(sys.stdin.read()))