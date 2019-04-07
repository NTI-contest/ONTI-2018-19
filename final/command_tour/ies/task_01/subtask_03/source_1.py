import ips
psm = ips.init()

def average_weather(type, turn):
    if type == 'sun':
        q = psm.sun[turn].forecast
        return (0.25 * (q.lower0 * 0.5 + q.lower50 + q.median + q.upper50 + q.upper0 * 0.5))
    else:
        q = psm.wind[turn].forecast
        return (0.25 * (q.lower0 * 0.5 + q.lower50 + q.median + q.upper50 + q.upper0 * 0.5))

main_station = list(psm.stations.keys())
buffer = ips.buffer()
turn = psm.get_move()
clients = psm.powersystem.get_all_clients()
first_turn = 1
last_turn = 50
next_turn = turn + 1

def wind_koeff(turn):
    return 0.9

sun_koeff = 1  # Зависимость мощности панелей от солнца
current_consumption = 0  # Текущее производство
current_production = 0  # Текущее потребление
panels = 1  # Кол-во панелей
turbines = 0  # Кол-во турбин
trade10_koeff = 1  # Какую часть средней разницы энергии отправлять на биржу через 10 ходов
comments = True  # Включены ли комментарии выполненных скриптом действий
ips.set_order_trace(True)
average_estimated_production = [0] * 16
average_estimated_consumption = [0] * 16

def est_cons(turn):
    cons = 0
    clients = psm.powersystem.get_all_clients()
    for client in clients:
        if client.is_consumer():
            cons += ((client.preset[turn][0] + client.preset[turn][1]) / 2)
    for offer in psm.exchange:
        if offer.owner == psm.you:
            if offer.issued + offer.exchange == turn:
                if offer.amount > 0:
                    cons += offer.amount
    return cons

def est_prod(turn):
    prod = 0
    prod += (wind_koeff(turn) * average_weather('wind', turn) * turbines)
    prod += (sun_koeff * average_weather('sun', turn) * panels)
    for offer in psm.exchange:
        if offer.owner == psm.you:
            if offer.issued + offer.exchange == turn:
                if offer.amount < 0:
                    prod -= offer.amount
    return prod

for client in clients:
    if client.is_consumer():
        current_consumption += abs(client.power[-1])
    else:
        current_production += abs(client.power[-1])

for offer in psm.exchange:
    if offer.owner == psm.you:
        if offer.issued + offer.exchange == turn:
            if offer.amount > 0:
                current_consumption += offer.amount
            else:
                current_production -= offer.amount

average_estimated_consumption[0] = current_consumption
average_estimated_production[0] = current_production
for i in range(1, 16):
    average_estimated_production[i] = 1
    average_estimated_consumption[i] = 1

if turn < last_turn - 10:
    shortage10 = average_estimated_consumption[10] - average_estimated_production[10]
    if shortage10 > 0:
        psm.orders.trade10.buy(shortage10)
        print('buying in 10 turns', shortage10)
    elif shortage10 < 0:
        psm.orders.trade10.sell(-shortage10)
        print('selling in 10 turns', -shortage10)

for client in clients:
    if client.is_generator():
        if 'solar' in str(client):
            solar_out = client.power[-1]
        # print(client.addr, 'generating', client.power[-1])
    elif client.is_consumer():
        pass
        # print(client.addr, 'consuming', client.power[-1])
    else:
        pass
        # print('unknown', client.addr)
if solar_out > 0:
    real_sun_k = psm.sun[turn].value / solar_out
    print('sun koeff =', real_sun_k)

if last_turn - turn > 17:
    z = 16
else:
    z = last_turn - turn - 2
for i in range(1, z):
    shortage = average_estimated_consumption[i] - average_estimated_production[i]
    if shortage > 25:
        print('critical: in', i, 'turns shortage', shortage, 'МВт', 'order already placed for')
    elif shortage < -25:
        print('critical: in', i, 'turns overgeneration', -shortage, 'МВт')
    elif shortage > 15:
        print('warning: in', i, 'turns shortage', shortage, 'МВт')
    elif shortage < -15:
        print('warning: in', i, 'turns overgeneration', -shortage, 'МВт')
if last_turn - turn > 5:
    z = 4
else:
    z = 0
for i in range(4):
    shortage = average_estimated_consumption[i] - average_estimated_production[i]
    if shortage > 0:
        print('In', i, 'turns shortage', shortage, 'МВт')
    else:
        print('In', i, 'turns overgeneration', -shortage, 'МВт')

for offer in psm.exchange:
    if offer.owner == psm.you:
        if offer.amount > 0:
            print(offer.amount, 'will be bought in', offer.issued - offer.exchange - turn, 'turn(s)')
        else:
            print(offer.amount, 'will be sold in', offer.issued - offer.exchange - turn, 'turn(s)')
