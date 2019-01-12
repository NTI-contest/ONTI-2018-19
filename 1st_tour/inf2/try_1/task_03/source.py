from decimal import Decimal

x1, y1, z1 = [Decimal(i) for i in input().split()]
x2, y2, z2 = [Decimal(i) for i in input().split()]
x3, y3, z3 = [Decimal(i) for i in input().split()]
a = ((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1)).sqrt()
b = ((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2) + (z3 - z2) * (z3 - z2)).sqrt()
c = ((x3 - x1) * (x3 - x1) + (y3 - y1) * (y3 - y1) + (z3 - z1) * (z3 - z1)).sqrt()
p = (a + b + c) / 2
print((p * (p - a) * (p - b) * (p - c)).sqrt())