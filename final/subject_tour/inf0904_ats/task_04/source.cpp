#define _CRT_SECURE_NO_WARNINGS 

#include <string> 
#include <stdio.h> 
#include <cstdio> 
#include <iostream> 
#include <vector> 
#include <queue> 
#include <algorithm>


int main()
{
    int m = 0;
    int n = 0;
    scanf("%d %d", &m, &n);
    std::vector<float> busy;
    std::vector<float> busy_sum;
    busy.resize(m);
    busy_sum.resize(m + 1);
    for (int i = 0; i < m; i++)
        scanf("%f", &busy[i]);
    std::sort(busy.begin(), busy.end());

    busy_sum[0] = 0;
    for (int i = 1; i <= m; i++)
        busy_sum[i] = busy_sum[i - 1] + busy[i - 1];

    for (int i = 0; i < n; i++)
    {
        int min = 0;
        int max = 0;
        scanf("%d %d", &min, &max);


        min = m - min + 1;
        max = m - max + 1;
        if (min > max)
            std::swap(min, max);


        float res = (busy_sum[max] - busy_sum[min - 1]) / (float)(max - min + 1);
        printf("%.4f\n", res);
    }
}