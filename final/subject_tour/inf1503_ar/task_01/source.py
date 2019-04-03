def distance(planet1, planet2):
    d = [(i - j) ** 2 for i, j in zip(planet1, planet2)]
    return sum(d) ** 0.5


def find_nearest(planet, planets, visited):
    min_distance = 10 ** 6
    nearest = None
    for i, p in enumerate(planets):
        if visited[i]:
            continue
        d = distance(planet, p)
        if d < min_distance:
            min_distance = d
            nearest = i
    visited[nearest] = True
    return nearest


n = int(input())
s, e = list(map(int, input().split()))

planets = []
for _ in range(n):
    planets.append(list(map(int, input().split())))

visited = [False] * n
visited[s] = True

steps = 0
while s != e:
    s = find_nearest(planets[s], planets, visited)
    steps += 1

print(steps)
