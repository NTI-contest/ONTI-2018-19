# put your python code here


import numpy as np

def neighbours(i, j):
    return [i-1, j], [i+1, j], [i, j-1], [i, j+1]

def read_sequence(m, i, j, sequence):
    sequence.append(m[i][j])
    m[i][j] = 0
    for ni, nj in neighbours(i, j):
        if m[ni][nj] != 0:
            read_sequence(m, ni, nj, sequence)

h, w = map(int, input().split())
m = []

for i in range(h):
    line = map(int, input().split())
    m.append(list(line))

sequences = []
for i in range(h):
    for j in range(w):
        if m[i][j] != 0:
            sequence = []
            read_sequence(m, i, j, sequence)
            sequences.append(sorted(sequence))

max_len = 0
index = 0
for i, sequence in enumerate(sequences):
    ln = len(sequence)
    if ln == max_len:
        if sum(sequence) > sum(sequences[index]):
            max_len = 0
    if ln > max_len:
        max_len = ln
        index = i

for value in sequences[index]:
    print(value)

