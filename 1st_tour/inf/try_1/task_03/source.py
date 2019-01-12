import sys
         
def solve():
    dataset = sys.stdin.read()
    input = dataset.split()
    n = int(input[0])
    s1, s2 = input[1:]

    p = 0
    
    for i in range(n):
        if s1[i] != s2[i]:
            p += 1
        
    print(p / n)