Y, BB, P, N = [int(v) for v in input().split()]
measurements = [int(v) for v in input().split()]


def zone(BT):
    I = (BT - BB) / (220.0 - Y - BB)
    if I < 0:
        return 'LAST ELEMENT HACK'
    elif 0.0 <= I <= 0.50:
        return 'RELAXING'
    elif 0.50 < I <= 0.60:
        return 'VERY LIGHT'
    elif 0.60 < I <= 0.70:
        return 'LIGHT'
    elif 0.70 < I <= 0.80:
        return 'MODERATE'
    elif 0.80 < I <= 0.90:
        return 'HARD'
    else:
        return 'MAXIMUM'


zone_prev = zone(measurements[0])
zone_repeats = 0
for BT in measurements + [-99999]:
    zone_curr = zone(BT)
    if zone_curr == zone_prev:
        zone_repeats += 1
    else:
        print(zone_prev, zone_repeats * P)
        zone_repeats = 1
    zone_prev = zone_curr
