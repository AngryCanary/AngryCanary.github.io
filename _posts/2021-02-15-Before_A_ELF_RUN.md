---
author: AngryCanary
tags: Misc_Tricks
typora-root-url: ..\assets\link
---



# The Step Before An ELF Running.

## 							在事发之前的小故事. （During Coding To ELF Generate）

```  apl
从小到大 ，当你第一次学到C语言的时候，你自豪的写下HelloWorld.C的时候，你或许看到以下内容。

敲代码(Coding) -> 预处理 (PreProcessor) -> 编译 (Compiler) -> 汇编(Assmbler) -> 链接(Linker)

HelloWorld.C -> HelloWorld.i -> HelloWorld.S -> HelloWorld.O -> HelloWorld

随后你编写的伟大的HelloWorld将会运行，你将会自豪的看到你期待的 Hello World !

然后或许此时一个问号打在了公屏上 ，发生甚么事了？
```



## Coding:

```
 这一步 我们将凭借自己的聪明才智。编写出了HelloWorld.C
```

![SourceCode]({{ site.url }}/assets/link/HelloWorld_C.png)

## PreProcessor: 

-E  Preprocess only; do not compile, assemble or link.

```
这一步 预处理器 对你的源码进行了处理. 目的是将更人性化的语法处理一下 更符合机器需求的
			 对#include的头文件进行包含处理
			 对#define系列的定义进行必要的增删
			 等等操作...
```

![HelloWorld_i.png]({{ site.url }}/assets/link/pp_i.png)

## Compiler:

-S  Compile only; do not assemble or link.

```
这一步将被处理过的源码文件进行编译处理 ， 编译成为Asm.
```

![Compile]({{ site.url }}/assets/link/Compile.png)

## Assmbler:

-c  Compile and assemble, but do not link.

```
 汇编 生成 可重定位目标文件 与最终Linker生成的ELF还是有一定区别，让我们继续看看。
```

![asm1]({{ site.url }}/assets/link/asm1.png)

![asm2]({{ site.url }}/assets/link/asm2.png)

# Linker:

```
对可重定位目标文件 进行链接.
	 静态链接 / 动态链接 。
```

![Link1]({{ site.url }}/assets/link/Link1.png)

```assembly
最终ELF 中 Main的反汇编. 与Asm后产生的单个可重定位目标文件不同。
例如:

115c:	48 8d 3d a1 0e 00 00 	lea    0xea1(%rip),%rdi        # 2004 <_IO_stdin_used+0x4>
1163:	b8 00 00 00 00       	mov    $0x0,%eax
1168:	e8 e3 fe ff ff       	callq  1050 <printf@plt>

13:	48 8d 3d 00 00 00 00 	lea    0x0(%rip),%rdi        # 1a <main+0x1a>
1a:	b8 00 00 00 00       	mov    $0x0,%eax
1f:	e8 00 00 00 00       	callq  24 <main+0x24>

这就涉及到 Position-Independent Code .

Link过程中符号的解析 以及 定位的时候 关于不同节区跳转的故事。

在生成 可重定位目标文件的这一个环节 ， 各文件相对孤立 。 符号还没有解析，Assmbler 为 未解析的符号留下占位符。等待之后Linker的处理。并留下重定位条目。

诸如.rel.text .rel.data 段 

```

```c
typedef struct{
    long offset; // Relative Offset
    long type; // Like R_X86_64_PC32 // R_X86_64_32 Relative Or Absolute
    long symbol; // the symbol's string . Symbol Table Index
    long addend; //Some Changes . In my oninion . to fill the gap between Opcode and Next Instruction.
}Elf64_Rela; //重定位条目信息结构体
```

```c
//Reloc Pseudo Code
Section S;
Elf64_Rela Victim;
void* TargetAddr = Victim.offset + S;
if(Victim.type == R_X86_64_PC32){
    *TargetAddr = Address(Victim.Symbol) + Victim.addend - (TargetAddr); //Relative
}else if(==R_X86_64_32){
    *TargetAddr = Address(Victim.Symbol) + Victim.addend; //Absolute
}

```

```
静态链接: 将不同的 objective file 连起来 。 
动态链接：先进行一些简单的链接(plt && got) 在运行的时候根据需要动态的链接. FULL RELEO OR Partical RELRO .  Lazy Bind 等等机制
```

```asm
Partial RELRO: 
	Linux Version : Ubuntu 20.04
	新版本采用了INTEL的CET技术 。 也加入了.plt.sec 段。
	开启Partial RELRO 的同时也就开启了 Lazy Bind。
	
	在第一次调用Extern 的函数时:
		.plt.sec(funcion) -> .plt(function) -> .plt[0] -> dl_runtime_resolve
            PLT[0] -> CALL _dl_runtime_resolve
            GOT[0] -> Relatavie offset of .dynamic
            GOT[1] -> Addr of reloc entries
            GOT[2] -> Addr of _dl_runtime_resolve
```

```asm
.plt.sec section
    进一步增加这个过程的安全性？ 在plt.sec段进行CS:GOT[function] 的 JMP 操作。
.plt section
	未绑定之前GOT 里存的 是 .plt[function]
	进入后执行
	push Function_Idx
	jmp plt[0]
	PLT[0] 是一个 特殊的 PLT表位置 -> 用来调用 动态链接器 _dl_runtime_resolve
	PLT[0] Instruction:
	push cs:GOT[1]
	jmp  cs:GOT[2] 
	//传入了 GOT[0] + GOT[1] 两个参数 然后就JMP 过去了 就开始 _dl_runtime_resolve
```

## _dl_runtime_resolve  动态链接器的跟进分析 :

```asm
#在 CALL 了 GOT[2] 中储存的 函数 地址 后 就进入了 _dl_runtime_resolve 的环节.
在32位的环境中 _dl_runtime_resolve
在64位的环境中 _dl_runtime_resolve_xsave  大致是寄存器的恢复储存方式有区别?
区别在一些宏的定义. 这里用64位的分析.
```

```asm

push    rbx   # 首先保留现场
 mov     rbx, rsp
 and     rsp, 0FFFFFFFFFFFFFFC0h
 sub     rsp, cs:qword_7FB52A1AFD50
 mov     [rsp], rax
 mov     [rsp+8], rcx
 mov     [rsp+10h], rdx
 mov     [rsp+18h], rsi
 mov     [rsp+20h], rdi
 mov     [rsp+28h], r8
 mov     [rsp+30h], r9
 mov     eax, 0EEh
 xor     edx, edx
 mov     [rsp+250h], rdx
 mov     [rsp+258h], rdx
 mov     [rsp+260h], rdx
 mov     [rsp+268h], rdx
 mov     [rsp+270h], rdx
 mov     [rsp+278h], rdx
 xsavec  byte ptr [rsp+40h]
 mov     rsi, [rbx+10h] # 这里是之前call 之前传入的 idx
 mov     rdi, [rbx+8]  #这个是GOT[1] // 是 reloc entry 的地址
 call    near ptr _dl_fixup #关键call 之 _dl_fixup
 mov     r11, rax  #_dl_fixup return Target Function Addr . Restore in R11
 mov     eax, 0EEh  #恢复现场
 xor     edx, edx
 xrstor  byte ptr [rsp+40h]
 mov     r9, [rsp+30h]
 mov     r8, [rsp+28h]
 mov     rdi, [rsp+20h]
 mov     rsi, [rsp+18h]
 mov     rdx, [rsp+10h]
 mov     rcx, [rsp+8]
 mov     rax, [rsp]
 mov     rsp, rbx
 mov     rbx, [rsp]
 add     rsp, 18h
 bnd jmp r11 # jmp Target Function Addr.
```

```asm
//核心的重定位在fixup里 分析一下源码. 以及相关数据结构。
//相关数据结构 及 段 内容	
    
typedef struct
{
  Elf32_Sword	d_tag;			/* Dynamic entry type */ 区别不同的入口的标签
  union
    {
      Elf32_Word d_val;			/* Integer value */ 
      Elf32_Addr d_ptr;			/* Address value */  //存一个Size值或者是ptr
    } d_un;
} Elf32_Dyn; 这里是.dynamic 段 的数据结构 
```

```asm
.DYNAMIC Section
    			Elf64_Dyn <1, 1>        ; DATA XREF: LOAD:00000000000001A0↑o
                                         ; .got.plt:_GLOBAL_OFFSET_TABLE_↓o
                                         ; DT_NEEDED libc.so.6
                 Elf64_Dyn <0Ch, 1000h>  ; DT_INIT
                 Elf64_Dyn <0Dh, 11F8h>  ; DT_FINI
                 Elf64_Dyn <19h, 3DE8h>  ; DT_INIT_ARRAY
                 Elf64_Dyn <1Bh, 8>      ; DT_INIT_ARRAYSZ
                 Elf64_Dyn <1Ah, 3DF0h>  ; DT_FINI_ARRAY
                 Elf64_Dyn <1Ch, 8>      ; DT_FINI_ARRAYSZ
                 Elf64_Dyn <6FFFFEF5h, 3A0h> ; DT_GNU_HASH
                 Elf64_Dyn <5, 470h>     ; DT_STRTAB
                 Elf64_Dyn <6, 3C8h>     ; DT_SYMTAB
                 Elf64_Dyn <0Ah, 84h>    ; DT_STRSZ
                 Elf64_Dyn <0Bh, 18h>    ; DT_SYMENT
                 Elf64_Dyn <15h, 0>      ; DT_DEBUG
                 Elf64_Dyn <3, 4000h>    ; DT_PLTGOT
                 Elf64_Dyn <2, 18h>      ; DT_PLTRELSZ
                 Elf64_Dyn <14h, 7>      ; DT_PLTREL
                 Elf64_Dyn <17h, 5E8h>   ; DT_JMPREL
                 Elf64_Dyn <7, 528h>     ; DT_RELA
                 Elf64_Dyn <8, 0C0h>     ; DT_RELASZ
                 Elf64_Dyn <9, 18h>      ; DT_RELAENT
                 Elf64_Dyn <6FFFFFFBh, 8000000h> ; DT_FLAGS_1
                 Elf64_Dyn <6FFFFFFEh, 508h> ; DT_VERNEED
                 Elf64_Dyn <6FFFFFFFh, 1> ; DT_VERNEEDNUM
                 Elf64_Dyn <6FFFFFF0h, 4F4h> ; DT_VERSYM
                 Elf64_Dyn <6FFFFFF9h, 3> ; DT_RELACOUNT
                 Elf64_Dyn <0>           ; DT_NULL
```

```asm
.symtab 诸如此类
     Elf64_Sym <offset aPrintf - offset 0xb, 12h, 0, 0, offset dword_0,0>\ ; "printf"
#数据结构:
typedef struct
{
  Elf64_Word	st_name;		/* Symbol name (StrTab中字符串的偏移) */
  unsigned char	st_info;		/* Symbol type(Low4bit) and binding(High4bit)*/
  unsigned char st_other;		/* Symbol visibility * 仅使用Low 2 bit /
  Elf64_Section	st_shndx;		/* Section index */
  Elf64_Addr	st_value;		/* Symbol value */
  Elf64_Xword	st_size;		/* Symbol size */
} Elf64_Sym; 
#该ELFprintf st_name 偏移为0xb
#st_info = 0x12 -> 0001 0010 -> bind = 0x1(GlobalSymbol) Type = 0x2(Function)
#st_other 0 默认可见性
#st_shndx 0 未定义Section
#st_value st_size 均为0
```

```asm
.rel.plt
	#数据结构
typedef struct
{
  Elf64_Addr	r_offset;		/* Address */ 正常情况下指向GOT表
  Elf64_Xword	r_info;			/* Relocation type and symbol index */上面有讲 其实类型有很多
  # r_info 的 处理方式 High32 Sym Low32 Type   Sym -> 是对应符号在 symtab 的偏移 || Type 是 重定位类型
  # 创建 PLT 等待导入的 低32 写 7 。Link过程中解析好的 GOT 写 6 (AMD x86-64 relocations.)
  Elf64_Sxword	r_addend;		/* Addend */ 做一个偏移 加法。
} Elf64_Rela; // 和上面讲到的 类似~只不过symbol无了 原理一致。
#===========================额外写一下 r_info
# sym 偏移 x64 -> (TargetSymTab - Symtab) / 0x18
# r_info = ((TargetSymTab - Symtab) / 0x18 ) << 32 + 0x7 (Function)
//还是用 Printf 举个例子:
Elf64_Rela <4018h, 200000007h, 0> ; R_X86_64_JUMP_SLOT printf 
```



```asm
_dl_fixup (struct link_map *l, ElfW(Word) reloc_arg)
   //GOT[1] 就是 link_map l;
   //reloc_arg 就是传进去的 Index 
   //在_dl_fixup
```

