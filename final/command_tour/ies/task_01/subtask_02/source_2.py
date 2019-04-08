import powerbalance as p
# Импорт нашего же модуля
 
# Константы их правил
buyCost = 5
buyCostFast = 10
sellCost = 2
sellCostFast = 1
 
#Вычисление стоимости одного исхода энергобаланса
def makeCost(value,adjust):
    result = 0
    if adjust > 0:
        result -= adjust * buyCost
    else:
        result += adjust * sellCost
    diff = value + adjust
    if diff < 0:
        result += diff * sellCostFast
    else:
        result -= diff * buyCostFast
    return result
 
#Вычисление распределения вероятностей расходов/прибылей
def costBalance(power,adjust):
    return [ (makeCost(v,adjust),p) for (v,p) in power]
 
#Простой и глупый алгоритм жадного спуска
def greed(a,b,c,x):
    if b < a and b < c:
        return 0
    if b > a:
        return -x
    if b < c:
        return x
    else:
        return -x
 
#Находим какой-то из минимумов коррекции баланса энергосистемы
def greedilyFindAdjust(net):
    adjStep = 0.1
    adj = 0
    power = p.powerBalance(p.network)
    print('Preparations are complete')
    while True:
        g = greed(costBalance(power,adj-adjStep),costBalance(power,adj),
                  costBalance(power,adj+adjStep),adjStep)
        if g == 0:
            return adj
        else:
            print(adj)
            adj += g
 
#Напечатать результат
print(greedilyFindAdjust(p.network))
