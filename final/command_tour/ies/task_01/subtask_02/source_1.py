import operator as o
 
#Этот модуль будет использоваться почти во всех остальных решениях
 
#Операция на «нечётких множествах»
def fuzzyop(fuz1, fuz2, op):
    result = []
    for (val1,prob1) in fuz1:
        for (val2,prob2) in fuz2:
            result.append((op(val1,val2),prob1*prob2))
    return result
 
#Оптимизировать представление случайной величины
def squash(d):
    d.sort(key=lambda x: x[0])
    l=len(d)
    newD = []
    acc = 0
    for i in range(len(d)-1):
        if d[i][0] != d[i+1][0]:
            x = (d[i][0], acc+d[i][1] )
            newD.append(x)
            acc = 0
        else:
            acc += d[i][1]
    x = (d[len(d)-1][0], acc+d[len(d)-1][1])
    newD.append(x)
    return newD
 
#Округление по произвольной базе
def myround(value,step):
    mod = value % step
    div = value // step
    if mod > step / 2:
        return step * ( div + 1 )
    else:
        return step * div
 
#Огрубить случайную величину. чтобы ускорить вычисления
#Желательно также убирать вероятности ниже порогового значения
roughstep = 0.2
def rough(fuz):
    result = [(myround(val,roughstep),prob) for (val,prob) in fuz]
    return squash(result)
 
#Получить численную случайную величину из прогноза
stepsize = 0.1
def fromForecast(forecast):
    lower = forecast / 1.2
    upper = forecast / 0.8
    stepsLower = []
    x = forecast
    while x >= lower:
        stepsLower.append(x)
        x -= stepsize
    lowers = []
    for l in stepsLower:
        lowers.append((l,1/len(stepsLower)))
    stepsUpper = []
    x = forecast + stepsize
    while x <= upper:
        stepsUpper.append(x)
        x += stepsize
    uppers = []
    for l in stepsUpper:
        uppers.append((l,1/len(stepsUpper)))
    result = lowers + uppers
    return result
 
#Прочитать прогнозы ветра
with open('wind.txt') as f:
    tmp = f.read().splitlines()
    wind = [ eval(x) for x in tmp ]
 
#Прочитать прогнозы солнца
with open('sun.txt') as f:
    tmp = f.read().splitlines()
    sun = [ eval(x) for x in tmp ]
 
#Прочитать прогнозы потребления домов
with open('houses.txt') as f:
    tmp = f.read().splitlines()
    houses = [ eval(x) for x in tmp ]
 
#Прочитать прогнозы потребления заводов
with open('factories.txt') as f:
    tmp = f.read().splitlines()
    factories = [ eval(x) for x in tmp ]
 
#Прочитать прогнозы потребления больниц
with open('hospitals.txt') as f:
    tmp = f.read().splitlines()
    hospitals = [ eval(x) for x in tmp ]
 
#Линейные коэффициенты генерации для ветра и солнца
coefSun = [0.12, 0.94, 0.7]
coefWind = [0.09, 0.32, 0.49, 0.41, 0.27, 0.16]
 
# Вычисление прогноза генерации
def powerForecast(coefficients,values,tick):
    power = [(0,1)]
    for i in range(0,len(coefficients)):
        if tick-i < 0:
            val=0
        else:
            val=values[tick-i]
        part = fuzzyop(fromForecast(val),[(coefficients[i],1)],o.mul)
        power = fuzzyop(power,part,o.add)
    return rough(power)
 
# Вычисление прогноза генерации
def powerSun(tick):
    return powerForecast(coefSun,sun,tick)
 
# Вычисление прогноза генерации
linear = 0.44 #коэффициент при x^3
def powerWind(tick):
    tmp = powerForecast(coefWind,wind,tick)
    return [(max(15,linear*(x**3)),p) for (x,p) in tmp ]
 
class Network:
    houses = 0
    hospitals = 0
    factories = 0
    wind = 0
    solar = 0
    def __init__(self,h,f,b,w,s):
        self.houses = h
        self.hospitals = b
        self.factories = f
        self.wind = w
        self.solar = s
 
# Задаём состав сети
network = Network(2,2,1,1,2)
 
def powerBalance(net):
    power = [(0,1)]
    for tick in range(0,3):
        for _ in range(0,net.houses):
            power=fuzzyop(power,fromForecast(houses[tick]),o.sub)
        power=rough(power)
        for _ in range(0,net.factories):
            power=fuzzyop(power,fromForecast(factories[tick]),o.sub)
        power=rough(power)
        for _ in range(0,net.hospitals):
            power=fuzzyop(power,fromForecast(hospitals[tick]),o.sub)
        power=rough(power)
        for _ in range(0,net.solar):
            power=fuzzyop(power,powerSun(tick),o.add)
        power=rough(power)
        for _ in range(0,net.wind):
            power=fuzzyop(power,powerWind(tick),o.add)
    return rough(power)
 
def expect(fuz):
    result = 0
    for (v,p) in fuz:
        result += v*p
    return result

#Напечатать математическое ожидание энергетического баланса
print(expect(powerBalance(network)))
 