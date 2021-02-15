---
author: AngryCanary
layout: post
tags: Misc_Tricks
---

# catomic_compare_and_exchange_val_acq

## 																			gcc中的一个基础原子操作

```c
当前理解: 2021-2-15
因为进程 线程 内核 用户态等的存在 CPU核心在一个时钟单位只能执行一条指令
    由内核控制的上下文切换及调度决定了CPU内部在同一时间不断的切换来自不同上下文的命令。
    但在某些情况下程序迫切的需要在一次性CPU分配的时间单位内完成某个操作
    原子操作就诞生了。这种操作维护了线程的安全。
```

## GCC DEFINE

```c
x86
 #  define catomic_compare_and_exchange_val_acq(mem, newval, oldval) \
  __atomic_val_bysize (__arch_c_compare_and_exchange_val,acq,		      \
		       mem, newval, oldval)
# else
x64
#  define catomic_compare_and_exchange_val_acq(mem, newval, oldval) \
  atomic_compare_and_exchange_val_acq (mem, newval, oldval)
```

  catomic -> atomic

```c
- #define atomic_compare_and_exchange_val_acq(mem, newval, oldval) 
  ({ __typeof (mem) __gmemp = (mem);	//_gmemp = 转存mem			      
     __typeof (*mem) __gret = *__gmemp; // __gret 是 *_gmemp	      
     __typeof (*mem) __gnewval = (newval);// gnewval 转存 newval
    // newval 默认是mem的指针类型
								      
     if (__gret == (oldval))		// __gret == oldval 个人意见 oldval作为Check传入
       *__gmemp = __gnewval;		// *mem = newval			      
     __gret; })
// 判断*mem 是否 与 oldval相等 是的话 *mem = newval   
 
//Tips __typeof 关键字 获取mem的类型. 相当于动态改变此处类型

```

