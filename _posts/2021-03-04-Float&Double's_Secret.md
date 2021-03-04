---
author: AngryCanary
tag: Binary
layout: post
---

# Float & Double 的IEEE 规则

>前言: 好久没想，有点忘却。温故而知新下

## Float&Double 位数 以及构成

![p1]({{ site.url }}/assets/postimg/FandD/1.png)

>IEEE 浮点 采用 V = [(-1)^s ] * [2^E] *  M
>
>E 由 e阶码运算得到
>
>M 是一个二进制小数 范围 0 -> 1-e   ||   1 -> 2-e
>
>Float  -> 32Bits      Double -> 64Bits
>
>Float 1 + 8 + 23
>
>Double 1 + 11 + 52
>
>从高地址到低地址由三部分组成
>
>Sign 符号位置    Exponent 阶码      Significant  尾数
>
>S 符号位置  正数 0 负数 1
>
>e 阶码  E = e - biased = e - [ 2^(k-1) -1 ]  (非格式化时e = 1)
>
>frac 尾数 格式化是按照 1.x 中的 x 部分 非格式化是0.x部分

## 格式化 及 特殊值

![p2]({{ site.url }}/assets/postimg/FandD/2.png)

>阶码非全0或全1即 为 格式化
>
>阶码全0为非格式化 其作用是为了给趋近与0的数一个过渡 以及表示0 (格式化尾数默认省略小数点前的1)
>
>阶码全1 Frac全0  由符号位决定 正/负无穷大
>
>阶码全1 Frac!=0 表示 Not A Number (NaN)

## 表示范围及限制因素

>浮点数的范围从两方面考虑   精度 & 范围

### 精度

>精度由Frac字段决定 
>
>Float Frac字段 23bit  ->  2^23 = 8388608   23lg2 ≈ 6.92  保证6位 最大7位
>
>Double Frac字段 52bit ->  2^52 = 4503599627370496  52lg2 ≈ 15.65 保证15 最大 16位

指数范围

>指数范围由Exponent决定
>
>E算法上面提到过
>
>Float Exponent 8bit  E = (+127) - (-126)
>
>Double Exponent 11bit E = (+1023) - (-1022)