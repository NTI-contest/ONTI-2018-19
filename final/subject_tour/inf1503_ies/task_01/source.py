from math import e, pi, sqrt, trunc, log
import random

snowflakes = [ e / 12
             , pi / 22
             , e / ( pi ** 3 )
             , 0.04
             , 1/31
             , sqrt ( 1/999 )
             , sqrt (pi) / 48
             , 1/7
             , 0.2
             ]

snowflakes.append(1-sum(snowflakes))

def partSum(i):
    return sum(snowflakes[:i+1])

def findSmallDigitAndReduce(n):
    for i in range(10):
        if n < partSum(i):
            return (n-partSum(i-1),i)
    return None

def findLowerDigits(x,stahp):
    current = x
    result = []
    for _ in range(stahp):
        (newX,digit) = findSmallDigitAndReduce(current)
        current = newX / snowflakes[digit]
        result.append(digit)
    return result

onepow = 1 / snowflakes[0]

def findOrder(x):
    if x < 0:
        return 0
    else:
        return 1+trunc(log(x,onepow))

def gen():
    x = random.random()
    y = random.random()
    if y > 0.5:
        return x
    else:
        return 1/x

def generate():
    tests = []
    for _ in range(20):
        case = str(gen())
        tests.append(case)
    return "\n".join(tests) + "\n"

def solve(dataset):
    ones=dataset.splitlines(False)
    result = []
    for d in ones:
        result.append(d)
    return "\n".join(result)

def solve1(data):
    digits = data.replace(",",".")
    number = eval(digits)

    pw = findOrder(number)
    scaled = number / ( onepow ** pw )
    digits = findLowerDigits(scaled,10+pw)

    before = "".join(map(str,digits[:pw]))
    if len(before) == 0:
        before = "0"
    after  = "".join(map(str,digits[pw:]))

    return before + "." + after

def check(reply,clue):
    delta = 1e-10
    ours = [float(x) for x in clue.splitlines(False)]
    their = [float(x.replace(",",".")) for x in reply.splitlines(False)]
    if len(ours) != len(their):
        return False
    for i in range(len(ours)):
        if abs(their[i]-ours[i]) > 1e-10:
            return False
    return True

#Пример решения
#Можно получить из проверяющего добавлением к нему строки (если входные данные лежат в файле “in.txt”.

with open("in.txt") as fin:
    data = fin.read()
    print(solve(data))
