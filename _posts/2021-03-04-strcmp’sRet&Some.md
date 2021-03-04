---
author: AngryCanary
layout: post
tag: Misc
---



# Strcmp()  返回值 引发 的 思考惨案

>  • 0, if the s1 and s2 are equal;
>
>  • a negative value if s1 is less than s2;
>
>  • a positive value if s1 is greater than s2.
>            
> 实际上Strcmp的返回值是 第一次出现差值的位置 S1 对应 Byte - S2 对应位置的 Byte

## 对 if 的 真正判断机制的模糊 和 Strcmp 返回值 的 + - 0 三种结果 引爆炸弹

>因个人的错误理解。对IF判断的理解一直是>0 True <= 0 为 False
>直到今天遇到了

```c
if ( strcmp(s1, s) )
  {
    fwrite("[!] Passcode error!\n", 1uLL, 0x14uLL, stderr);
    exit(-1);
}
```

>
>  
>  我直接坏起来.  这之前是一个 随机数 + 溢出泄露的问题
>  虽然知道可以泄露 S 但是 错误的理解让我认为 只要 s1 比 s 小 也可以绕过. 可惜 不巧... 
>  耽误半天时间后意识到事情并不简单 瞅了一下汇编

```asm
.text:000055DBC1073603 0D8 E8 A8 FB FF FF                    call    _strcmp
.text:000055DBC1073608 0D8 85 C0                             test    eax, eax
.text:000055DBC107360A 0D8 74 2A                             jz      short loc_55DBC1073636
#靓仔突然意识到了一切....
```

```c
#test Eax , eax 
#jz     ->   经典EAX != 0 跳转环节
#已经够明显了。
```

# 总结

>C 中的判断实际上只有两种状态 
>0 -> False
>非0 -> True
>有符号数 将会被 当作 无 符号数 对待~  
>如果遇到语言上的奇怪问题 还是瞪一眼汇编吧