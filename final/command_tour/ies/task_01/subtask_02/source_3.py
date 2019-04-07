#Импортируем собственный модуль расчёта энергетического баланса
from powerbalance import *

#Импортируем собственный модуль расчёта экономического баланса
from costbalance import *
import operator as o
 
networkBefore = Network(2,2,1,1,2)
networkAfter = Network(2,2,1,1,3)
 
def findCumulativeCost(net1,net2):
    before = costBalance(networkBefore)
    after = costBalance(networkAfter)
    powerBefore = powerBalance(networkBefore)
    powerAfter = powerBalance(networkAfter)
    if net1.solar + net1.wind != net2.solar + net2.wind:
        return fuzzyop((fuzzyop(after,before,o.sub)),(fuzzyop(powerBefore,powerAfter,o.sub)),o.div)
    else:
        return fuzzyop(fuzzyop(after,before,o.sub),[(168,1)],o.div)
 
print(findCumulativeCost(networkBefore,networkAfter))
