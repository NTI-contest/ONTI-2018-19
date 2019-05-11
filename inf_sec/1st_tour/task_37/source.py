from pwn import *

conn = remote("prefix.2018.cyberchallenge.ru", 9001)
conn.recvlines(timeout=1)

def check(guess):
    conn.sendline(guess)
    return b"Yes" in conn.recvline(timeout=1)

alpha = "}abcdefghijklmnopqrstuvwxyz_1234567890"
guess = list("CC{")

while guess[-1] != '}':
    guess.append('}')
    for c in alpha:
        guess[-1] = c
        if check("".join(guess)):
            print(guess)
            break;

print("".join(guess))