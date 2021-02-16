---
author: AngryCanary
layout: post
tag: Glibc_Resolve
---



# How does Malloc Init?

> 小时候，我曾经把现成的Arena用的顺理成章，我曾经认为GDB就理所应当神奇的自动定位到每个堆块，自动分析出每个堆块的属性..等等
>
> 后来我长大了，世界也不是那么理所当然了。

##  _malloc_hook

```c
void *weak_variable (*__malloc_hook)
  (size_t __size, const void *) = malloc_hook_ini;
//malloc.c 1892
```

>初始化是通过 Malloc_Hook 进行的 。
>
>很容易联想到__libc_malloc 中 先进行的 Hook Check
>
>默认的Hook 并 不是空的。
>
>而是被初始化指向了 malloc_hook_init . 
>
>这里用Malloc列举.其他的都是同原理.
>
>Malloc Realloc Memalign 都最终调用了 ptmalloc_init

## malloc_hook_ini()


```c
static void *
malloc_hook_ini (size_t sz, const void *caller)
{
  __malloc_hook = NULL; // 清空钩子.
  ptmalloc_init (); //进行初始化 
  return __libc_malloc (sz); //初始化后再次调用
   //其他同理
}

static void *
realloc_hook_ini (void *ptr, size_t sz, const void *caller)
{
  __malloc_hook = NULL;
  __realloc_hook = NULL;
  ptmalloc_init ();
  return __libc_realloc (ptr, sz);
}

static void *
memalign_hook_ini (size_t alignment, size_t sz, const void *caller)
{
  __memalign_hook = NULL;
  ptmalloc_init ();
  return __libc_memalign (alignment, sz);
}
//in hooks.c + 27 
```

## Ptmalloc_Init()

```c
if (__malloc_initialized >= 0)
    return;

  __malloc_initialized = 0;
//首先清空malloc初始化标识. 并防止再次初始化

//暂不分析 涉及到 共享库运行的部分。共享库运行细节了解后再补充

  thread_arena = &main_arena;

  malloc_init_state (&main_arena);
//初始化 的对象是main_arena 
/*
static struct malloc_state main_arena =
{
  .mutex = _LIBC_LOCK_INITIALIZER,
  .next = &main_arena,
  .attached_threads = 1
}; 默认main_arena 只有这三个初始化了。
剩下的在 malloc_init_state里初始化。
*/
// malloc.c 1786
 TUNABLE_GET (check, int32_t, TUNABLE_CALLBACK (set_mallopt_check));
  TUNABLE_GET (top_pad, size_t, TUNABLE_CALLBACK (set_top_pad));
  TUNABLE_GET (perturb, int32_t, TUNABLE_CALLBACK (set_perturb_byte));
  TUNABLE_GET (mmap_threshold, size_t, TUNABLE_CALLBACK (set_mmap_threshold));
  TUNABLE_GET (trim_threshold, size_t, TUNABLE_CALLBACK (set_trim_threshold));
  TUNABLE_GET (mmap_max, int32_t, TUNABLE_CALLBACK (set_mmaps_max));
  TUNABLE_GET (arena_max, size_t, TUNABLE_CALLBACK (set_arena_max));
  TUNABLE_GET (arena_test, size_t, TUNABLE_CALLBACK (set_arena_test));
# if USE_TCACHE
  TUNABLE_GET (tcache_max, size_t, TUNABLE_CALLBACK (set_tcache_max));
  TUNABLE_GET (tcache_count, size_t, TUNABLE_CALLBACK (set_tcache_count));
  TUNABLE_GET (tcache_unsorted_limit, size_t,
	       TUNABLE_CALLBACK (set_tcache_unsorted_limit));
# endif
  TUNABLE_GET (mxfast, size_t, TUNABLE_CALLBACK (set_mxfast));
//一些列TUNABLE_GET 是通过环境变量设置一些参数
```

## Malloc_Init_State()

> 大部分的初始化工作在这里
>
> 从TOP 位置 作为第一个BIN位置 首先进行双向链表的初始化
>
> 

```c
static void
malloc_init_state (mstate av)
{
  int i;
  mbinptr bin;

  /* Establish circular links for normal bins */
  for (i = 1; i < NBINS; ++i)
    {
      bin = bin_at (av, i);
      bin->fd = bin->bk = bin;
    }

#if MORECORE_CONTIGUOUS
  if (av != &main_arena)
#endif
  set_noncontiguous (av);
  if (av == &main_arena)
    set_max_fast (DEFAULT_MXFAST); // 设置global_max_Fast
  atomic_store_relaxed (&av->have_fastchunks, false);//标志位清0

  av->top = initial_top (av); // 初始化TopChunk
// 因此 TopChunk有机会指向UnsortedBin
// 通过某些手段可以申请到Main_Arena的部分
//#define initial_top(M)  (unsorted_chunks (M))
}
//malloc.c 1833
```

