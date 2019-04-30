# Читаем данные из входного потока, как описано в задании
N, M = input().split()
N, M = int(N), int(M)
K = int(input())
begin = [[int(i) for i in input().split()] for i in range(K)]
end = [[int(i) for i in input().split()] for i in range(K)]

def sorting(a):  # функция сортировки по типу груза в ячейке
    return a[2]

begin.sort(key=sorting)
end.sort(key=sorting)

for i in range(K):
    # Не пытаемся переставлять, если та же позиция
    if begin[i][0] == end[i][0] and begin[i][1] == end[i][1]:
        continue
    print('M' + str(begin[i][0]) + ',' + str(begin[i][1]))
    print('G')
    print('M' + str(end[i][0]) + ',' + str(end[i][1]))
    print('P')