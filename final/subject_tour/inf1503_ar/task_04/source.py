import math

def distance(p1, p2):
    d = [(i - j) ** 2 for i, j in zip(p1, p2)]
    return sum(d) ** 0.5

def hit_point(p1, p2):
    hit_x = 0
    hit_y = p1[1] + (p2[1] - p1[1]) * 2
    hit_z = p1[2] + (p2[2] - p1[2]) * 2
    return hit_x, hit_y, hit_z

def linear_size(angular_size, distance):
    angular_size = math.radians(angular_size)
    return 2 * distance * math.sin(angular_size / 2)


n = int(input())
h = int(input())

start_point = list(map(int, input().split()))

holes = []

for _ in range(h):
    holes.append(list(map(int, input().split())))

hits = []
for _ in range(n):
    ball = list(map(int, input().split()))
    size = linear_size(ball[-1] / 60, 50)
    hits.append([hit_point(ball[:3], start_point), size])


passed = 0
for hit in hits:
    for hole in holes:
        d = distance(hole[:3], hit[0])
        if hole[-1] > (d + hit[1]):
            passed += 1

print(passed)
