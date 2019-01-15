import sys
import string

def z_func(s):
    i, slen = 1, len(s)
    out = [0] * slen
    out[0] = slen
    while i < slen:
        left, right = 0, i
        while right < slen and s[left] == s[right]:
            left += 1
            right += 1
        out[i] = left
        i += 1
    return out           
            
dataset = sys.stdin.read()
s, t = dataset.split()
listz = z_func(s + '#' + t + t[:-1])

lt = len(t)
ls = len(s)

list = [idx - lt - 1 for idx in range(lt + ls + 1) if lt == listz[idx]]

if len(list) == 0:
    list = [-1]

print(list[0])