---
layout: post
author: AngryCanary
tag: Glibc_Resolve
---

# Glibc Resolve-Malloc.c-OverView

### Malloc.c Standard Function:

```c

Standard (ANSI/SVID/...)  functions:
    malloc(size_t n);   // 申请N大小的堆快
    calloc(size_t n_elements, size_t element_size); // 在Malloc基础上 ClearContent> 与最终还是依靠Malloc 实现
    free(void* p); //Freeeeeee
    realloc(void* p, size_t n); // ”Multi-Function“ 重分配函数
    memalign(size_t alignment, size_t n);  //内存对齐
    valloc(size_t n);  // ? 某种过时的页面对齐分配方式？ /* Allocate SIZE bytes on a page boundary.  */
    mallinfo() // ？Info 顾名思义
    mallopt(int parameter_number, int parameter_value)
```

### Malloc.c Vital Statistics：

```c
Supported pointer representation:       4 or 8 bytes
Supported size_t  representation:       4 or 8 bytes
Alignment:  2 * overhead Size_t:
    
```



### Truth Call Of Base Function

```c
At the end of Malloc.c You Can See:
weak_alias (__malloc_info, malloc_info)
strong_alias (__libc_calloc, __calloc) weak_alias (__libc_calloc, calloc)
strong_alias (__libc_free, __free) strong_alias (__libc_free, free)
strong_alias (__libc_malloc, __malloc) strong_alias (__libc_malloc, malloc)
strong_alias (__libc_memalign, __memalign)
weak_alias (__libc_memalign, memalign)
strong_alias (__libc_realloc, __realloc) strong_alias (__libc_realloc, realloc)
strong_alias (__libc_valloc, __valloc) weak_alias (__libc_valloc, valloc)
strong_alias (__libc_pvalloc, __pvalloc) weak_alias (__libc_pvalloc, pvalloc)
strong_alias (__libc_mallinfo, __mallinfo)
weak_alias (__libc_mallinfo, mallinfo)
strong_alias (__libc_mallopt, __mallopt) weak_alias (__libc_mallopt, mallopt)
weak_alias (__malloc_stats, malloc_stats)
weak_alias (__malloc_usable_size, malloc_usable_size)
weak_alias (__malloc_trim, malloc_trim)

Like Malloc is Strong_Aliased To -> __libc_malloc
Almost Every  symbol -> __libc_symbol
```

### Malloc.c_Function_Resolve.
```c
malloc(): ->    
```

