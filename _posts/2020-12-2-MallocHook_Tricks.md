pwn的堆栈平衡



![img](https://img2018.cnblogs.com/i-beta/1755571/202002/1755571-20200208190139044-1751628967.png)



在Ret回上一层的时候要保证ESP指向压入栈的地址。

经过肆意的控制RIP之后程序可能栈与最开始接管的时候有所不同。可以通过额外添加更多的RET来 POP RIP 。

RET 加在ROP 之前不会造成任何奇怪的影响

Tricks：

```
打Malloc_Hook  - 0x23        选择 “\x00” * 0xB + p64(OneGadGet) + p64(Realloc+0x2)
Realloc + 2 错位 POP 帮助我们拿下
```

