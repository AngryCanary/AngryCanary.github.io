---
author: Canary
tag: Algorithm
---



#### [74. 搜索二维矩阵](https://leetcode-cn.com/problems/search-a-2d-matrix/)

难度中等365收藏分享切换为英文接收动态反馈

编写一个高效的算法来判断 `m x n` 矩阵中，是否存在一个目标值。该矩阵具有如下特性：

- 每行中的整数从左到右按升序排列。
- 每行的第一个整数大于前一行的最后一个整数。

 

**示例 1：**

![img](https://assets.leetcode.com/uploads/2020/10/05/mat.jpg)

```
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true
```

**示例 2：**

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2020/11/25/mat2.jpg)

```
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
输出：false
```

 

**提示：**

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-104 <= matrix[i][j], target <= 104`

```C++
#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        // 获取 每一行的个数 
        int nRaw=0,nColume=0;
        nRaw = matrix.size();
        nColume = (matrix.front()).size();
        // 获取每一行最后一个
        int Traw = -1;

        for(int i=0;i<nRaw;i++){
            vector<int> TempRaw = matrix.at(i);
            if(TempRaw.back()>=target){
                Traw = i;
                for(int ii=0;ii<nColume;ii++){
                    if(TempRaw.at(ii)==target)
                    return 1;
                }
        }
        // 若大 跳出第一个循环
    } 
    
}
};
```

