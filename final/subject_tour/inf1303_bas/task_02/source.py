n = input()
h = int(n[0:2])
m = int(n[2:4])
nh = h
nm = m + 1

if nm == 60:
    nm = 0
    nh += 1

if nh >= 24:
    nh -= 24

lights = [line.split() for line in '''..... ..... ..... ..... ..... ..... ..... ..... ..... .....
.###. ...#. .###. .###. .#.#. .###. .###. .###. .###. .###.
.#.#. ...#. ...#. ...#. .#.#. .#... .#... ...#. .#.#. .#.#.
.#.#. ...#. .###. .###. .###. .###. .###. ...#. .###. .###.
.#.#. ...#. .#... ...#. ...#. ...#. .#.#. ...#. .#.#. ...#.
.###. ...#. .###. .###. ...#. .###. .###. ...#. .###. .###.
..... ..... ..... ..... ..... ..... ..... ..... ..... .....'''.split('\n')]

def diff(x, y):
    ans = 0
    for row in lights:
        for a, b in zip(row[x], row[y]):
            if a != b:
                ans += 1
    return ans

g = '{:02d}{:02d}'.format(nh, nm)
ans = 0

for x, y in zip(n, g):
    ans += diff(int(x), int(y))

print(ans)