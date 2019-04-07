import random
import sys

random.seed(6162)
SUITE_SIZE = 10

def generateTask():
    result = []
    resultSum = 0
    variantsCount = random.randint(7,10)
    for _ in range(variantsCount):
        (m,p,a) = genVariant()
        result.append((m,p,a))
        resultSum += m
    return resultSum, len(result), result

def printTask():
    s, l, r = generateTask()
    pass

def readTask(data):
    ps, *items_raw = data.splitlines(False)
    n, w = map(int, ps.split())
    items = [(int(p), a, b) for (p, a, b) in (i.split() for i in items_raw)]
    return items, w

def genVariant():
    money = random.randint(5,35)
    probprev = 0.2 + 0.2 * random.random()
    probafter = 0.9 + 0.1 * random.random()
    return (money,probprev,probafter)

def vector(size,num):
    result = []
    for i in range(size):
        result.append(((1 << i ) & num)>0)
    return result

def countVariant(variants,n):
    prod = 1
    summ = 0
    l = len(variants)
    for i in range(l):
        (m,p,a) = variants[i]
        if vector(l,n)[i]:
            prod *= (1-float(a))
            summ += int(m)
        else:
            prod *= (1-float(p))
    newFail = 1 - prod
    return summ, newFail

def all(variants,limit):
    bestProb = 1
    for i in range(2 ** len(variants)):
        score, fail = countVariant(variants,i)
        if score <= limit and fail < bestProb:
            bestProb = fail
    return bestProb

def generate_item():
    price = random.randint(5,35)
    x = random.random() * 0.2 + 0.2
    y = x * (random.random() * 0.9 )
    return "{} {:.4} {:.4}".format(price, x, y)

def generate_one():
    item_n = random.randint(7, 15)
    money = random.randint(100, 200)
    items = "\n".join(generate_item() for _ in range(item_n))
    return "{} {}\n{}\n".format(item_n, money, items)

def generate():
    return [generate_one() for x in range(SUITE_SIZE)]

def solve(dataset):
    #print(dataset)
    s,lim = readTask(dataset)
    _,p0 = countVariant(s,0)
    pMax = all(s,lim)
    #print(p0,pMax)
    return str(p0/pMax)

def check(reply, clue):
    try:
        your = float(reply)
        mine = float(clue)
        return abs(your-mine) <= 0.01
    except Exception as e:
        return False, "ошибка формата"

x1 = '7 91\n34 0.3694 0.1881\n6 0.3967 0.05904\n29 0.3629 0.3279\n18 0.4685 0.3988\n \
      7 0.251 0.2173\n15 0.4967 0.4916\n19 0.3923 0.09796\n'
x2 = '30 320\n33 0.3824 0.1641\n27 0.28 0.2045\n8 0.2727 0.03715\n16 0.3769 0.2285\n \
      31 0.2833 0.07882\n10 0.4299 0.3793\n19 0.3323 0.3034\n29 0.4066 0.3941\n10 \
      0.4703 0.07739\n27 0.3413 0.1661\n14 0.258 0.0139\n26 0.2661 0.1518\n29 0.3395 \
      0.291\n16 0.2516 0.1018\n13 0.2779 0.1294\n31 0.4401 0.3566\n14 0.2754 0.07968\n \
      33 0.3246 0.3212\n23 0.4771 0.3942\n13 0.4212 0.2745\n19 0.3201 0.2555\n5 \
      0.4157 0.006087\n34 0.4888 0.4167\n30 0.4451 0.06692\n16 0.2776 0.02759\n12 \
      0.2625 0.0521\n21 0.4434 0.1725\n35 0.4749 0.2688\n25 0.4311 0.202\n20 0.3104 0.2109\n'

print(solve(sys.stdin.read()))
