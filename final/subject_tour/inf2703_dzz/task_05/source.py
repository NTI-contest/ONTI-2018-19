ax, ay, sx, sy, lx, ly = list(map(int, input().split()))
n = int(input())

smap = [['x' for _ in range(sy)] for _ in range(sx)]

for _ in range(n):    
    bx, by = list(map(int, input().split()))

    for x in range(lx):
        line = input().split()

        if bx + x >= ax and bx + x < ax + sx:
            for y in range(ly):
                if by + y >= ay and by + y < ay + sy:
                    if smap[bx - ax + x][by - ay + y] == 'x':
                        smap[bx - ax + x][by - ay + y] = line[y]
            
for x in smap:
    for y in x:
        print('{}\t'.format(y))
    print('\n')                             
                                