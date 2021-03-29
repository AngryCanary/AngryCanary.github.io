---
author: Canary
tag: Algorithm
---



# Reverse bits of a given 32 bits unsigned integer.

Note:

Note that in some languages such as Java, there is no unsigned integer type. In this case, both input and output will be given as a signed integer type. They should not affect your implementation, as the integer's internal binary representation is the same, whether it is signed or unsigned.
In Java, the compiler represents the signed integers using 2's complement notation. Therefore, in Example 2 above, the input represents the signed integer -3 and the output represents the signed integer -1073741825.
Follow up:

If this function is called many times, how would you optimize it?

 

Example 1:

Input: n = 00000010100101000001111010011100
Output:    964176192 (00111001011110000010100101000000)
Explanation: The input binary string 00000010100101000001111010011100 represents the unsigned integer 43261596, so return 964176192 which its binary representation is 00111001011110000010100101000000.
Example 2:

Input: n = 11111111111111111111111111111101
Output:   3221225471 (10111111111111111111111111111111)
Explanation: The input binary string 11111111111111111111111111111101 represents the unsigned integer 4294967293, so return 3221225471 which its binary representation is 10111111111111111111111111111111.


Constraints:

The input must be a binary string of length 32

```c++
#include<iostream>
using namespace std;
class Solution {

public:
    Solution(){
        reuint = 0;
    }
    uint32_t reuint;
    uint32_t reverseBits(uint32_t n) {
        for(int i=31;i>=0;i--){
         // 核心算法 原来的SHIFT多少位  RE+=(1<<(31-X)) && 每一次都 & 1<X-1
        
         reuint += (n>>i) <<(31-i);
         Debug(i,n>>i,n);
        n-=(n>>i)<<(i);
        }
    }
    void Debug(int i,int k,uint32_t n){
        cout << "此时计算位置为" << i << "当前位置" << k << "reuint当前值" << this->reuint <<"N剩余值:"<<n<< endl; 
    }
};

int main(){
    Solution* test = new Solution();
    test->reverseBits(43261596);
    printf("%d",test->reuint);
    return 1;
}
```

