import sys
def solve():
    dataset = sys.stdin.read()
    w1, w2 = dataset.split()
    w1 = w1.split('.') 
    w2 = w2.split('.') 
    
    a1 = int(''.join(w for w in w1))
    a2 = int(''.join(w for w in w2))
    
    d1 = 'N'
    d2 = 'E'
    if a1 < 0:
        d1 = 'S'
        a1 *= -1
    if a2 < 0:
        d2 = 'W'
        a2 *= -1
        
    x1 = a1 % 10000000
    x2 = a2 % 10000000
    
    a1 //= 10000000
    a2 //= 10000000
    
    x1 = x1 * 3600 // 10000000
    b1 = x1 // 60
    c1 = x1 % 60

    x2 = x2 * 3600 // 10000000
    b2 = x2 // 60
    c2 = x2 % 60

    ans = "{:02d}°{:02d}'{:02d}''{} {:02d}°{:02d}'{:02d}''{}\n".
        format(a1, b1, c1, d1, a2, b2, c2, d2)
    
    print(ans)