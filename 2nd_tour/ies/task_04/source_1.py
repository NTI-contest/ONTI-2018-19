import fileinput
import random
from math import sqrt, pi
import sys

k = 0.4
eff = 5

def part (d):
    sph = 4 * pi * d ** 2
    return eff / sph * k

def dist(X,Y,x,y):
    return sqrt((X-x)**2+(Y-y)**2)

def distH(X,Y,x,y):
    planar = dist(X,Y,x,y)
    spatial = dist(50,0,0,planar)
    return spatial

def powerPart(X,Y,x,y):
    return part((distH(X,Y,x,y)))

def circum1(Ax,Ay,Bx,By,Cx,Cy):
    a = sqrt((Ax-Bx)**2 + (Ay-By)**2)
    b = sqrt((Bx-Cx)**2 + (By-Cy)**2)
    c = sqrt((Cx-Ax)**2 + (Cy-Ay)**2)
    p = (a+b+c)/2
    r = a * b * c / 4 / sqrt ( p*(p-a)*(p-b)*(p-c) )
    x12 = Ax-Bx
    x23 = Bx-Cx
    x31 = Cx-Ax
    y12 = Ay-By
    y23 = By-Cy
    y31 = Cy-Ay
    z1 = Ax**2 + Ay**2
    z2 = Bx**2 + By**2
    z3 = Cx**2 + Cy**2
    z = x12 * y31 - y12 * x31
    zx = y12 * z3 + y23 * z1 + y31 * z2
    zy = x12 * z3 + x23 * z1 + x31 * z2
    rx = -zx / 2 / z
    ry = zy / 2 / z
    return r, rx, ry

def circum2(Ax,Ay,Bx,By,Cx,Cy):
    D = 2*(Ax*(By-Cy)+Bx*(Cy-Ay)+Cx*(Ay-By))
    Ux = ((Ax**2+Ay**2)*(By-Cy)+(Bx**2+By**2)*(Cy-Ay)+(Cx**2+Cy**2)*(Ay-By))/D
    Uy = ((Ax**2+Ay**2)*(Cx-Bx)+(Bx**2+By**2)*(Ax-Cx)+(Cx**2+Cy**2)*(Bx-Ax))/D
    return dist(Ux,Uy,Bx,By),Ux,Uy

def ctest():
    ax = random.random()
    ay = random.random()
    bx = random.random()
    by = random.random()
    cx = random.random()
    cy = random.random()
    d1,rx,ry = circum1(ax,ay,bx,by,cx,cy)
    d2,ux,uy = circum2(ax,ay,bx,by,cx,cy)
    if rx == ux and ry == uy:
        test()
    else:
        print("1da",dist(ax,ay,rx,ry))
        print("1db",dist(bx,by,rx,ry))
        print("1dc",dist(cx,cy,rx,ry))
        print("2da",dist(ax,ay,ux,uy))
        print("2db",dist(bx,by,ux,uy))
        print("2dc",dist(cx,cy,ux,uy))
        print("A",ax,ay)
        print("B",bx,by)
        print("C",cx,cy)
        print("R:",rx,ry)
        print("U:",ux,uy)

#ctest()

def covers(points,i1,i2,i3):
    Ax,Ay = points[i1]
    Bx,By = points[i2]
    Cx,Cy = points[i3]
    R,Ux,Uy = circum1(Ax,Ay,Bx,By,Cx,Cy)
    for p in range(len(points)):
        if p == i1 or p == i2 or p == i3:
            pass
        else:
            x,y = points[p]
            if dist(Ux,Uy,x,y) > R:
                return (False,None,None,None)
    return (True,R,Ux,Uy)

def findSmallestCover(points):
    best = float("inf")
    bX = None
    bY = None
    for i in range(len(points)-2):
        for j in range(i+1,len(points)-1):
            for k in range(j+1,len(points)):
                que,d,x,y = covers(points,i,j,k)
                #print("-> ",que,d,x,y)
                if que:
                    if best > d:
                        best = d
                        bX, bY = x,y
    return bX,bY,best

def ans(points):
    a,b,d = findSmallestCover(points)
    power = 1e3 / powerPart(0,0,0,d)
    return (a,b,power)

def readInput():
    count = None
    points = []
    for line in fileinput.input():
        if fileinput.isfirstline():
            count = eval(line)
        else:
            x,y = line.split()
            points.append((float(x),float(y)))
    return points

def test():
    points = readInput()
    x,y,d = findSmallestCover(points)
    print(x,y)

#test()

def readDataSet(dataset):
    count = None
    points = []
    for line in dataset.splitlines():
        #print(line)
        if count == None:
            count = eval(line)
        else:
            x,y = line.split()
            points.append((float(x),float(y)))
    return points

def generate():
    tests = []
    for _ in range(20):
        count = random.randint(4,20)
        result = "{}\n".format(count)
        for _ in range(count):
            x = random.random() * 2000 - 1000
            y = random.random() * 2000 - 1000
            result += "{} {}\n".format(x,y)
        tests.append(result)
    return tests

def solve(dataset):
    points = readDataSet(dataset)
    x,y,p = ans(points)
    return "{}".format(p)

def check(reply,clue):
    p = float(reply)
    P = float(clue)
    if abs(p-P)>=10:
        return False, "Мощность рассчитана неверно"
    return True

print(solve(sys.stdin.read()))