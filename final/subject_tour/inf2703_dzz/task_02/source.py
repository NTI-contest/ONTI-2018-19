def code(word):
    n = 4
    parts = [word[i:i+n] for i in range(0, len(word), n)]
    res = ''
    for p in parts:
        a = [int(digit) for digit in p]
        b = [(a[0] + a[1] + a[2]) % 2, (a[1] + a[2] + a[3]) % 2, 
            (a[0] + a[1] + a[3]) % 2]
        res += ''.join(str(x) for x in a + b)
    
    return res

def decode(word):
    n = 7
    parts = [word[i:i+n] for i in range(0, len(word), n)]
    res = ''
    for p in parts:
        a = [int(digit) for digit in p]
        b = a[4:]
        a = a[:4]
        
        s = [(a[0] + a[1] + a[2] + b[0]) % 2, (a[1] + a[2] + a[3] + b[1]) % 2, 
            (a[0] + a[1] + a[3] + b[2]) % 2]
        
        if s == [0, 1, 1]:
            a[3] = (a[3] + 1) % 2     
        elif s == [1, 0, 1]:
            a[0] = (a[0] + 1) % 2    
        elif s == [1, 1, 0]:
            a[2] = (a[2] + 1) % 2    
        elif s == [1, 1, 1]:
            a[1] = (a[1] + 1) % 2    

        res += ''.join(str(x) for x in a) 
    
    return res

def make_command(data):
    command, word = data[0], data[1]
    if (command == 'code'):
        return code(word)
    elif (command == 'decode'):
        return decode(word)
    return ''
    
n = int(input())

ans = ''

for i in range(n):
    line = input()
    ans += make_command(line.split()) + '\n'
    
print(ans)