import fileinput, math

coordinates = []
coordinates.append([])
i = 0
first_line = False
max_dist_allowed = 2.

def distance(x, y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)

f = fileinput.input()
f.readline()
f.readline()

for line in f:
    if len(line) > 1: 
        coordinates[i].append([float(f) for f in line.split(" ")])
    else:
        coordinates.append([])
        i += 1

min_distance = max_dist_allowed
frame = 0
frames_count = len(coordinates[0]) 
for i in range(len(coordinates)-1):
    for j in range(i+1, len(coordinates)):
        for k in range(frames_count):
            dist = distance(coordinates[i][k], coordinates[j][k])
            if (dist < min_distance):
                min_distance = dist
                frame = k
if min_distance == max_dist_allowed:
    print(-1)
else:
    print(min_distance, frame)