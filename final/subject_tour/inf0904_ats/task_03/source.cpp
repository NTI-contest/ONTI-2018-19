#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>


int main()
{
    std::vector<int> activeness(3600, 0);

    int n = 0;
    scanf("%d", &n);

    for (int i = 0; i < n; i++)
    {
        int g, y, r, ro;
        scanf("%d %d %d %d", &g, &y, &r, &ro);

        int time = r + ro;
        while (time < (int)activeness.size())
        {
            for (int j = time; j < std::min(time + g, (int)activeness.size()); j++)
                activeness[j]++;
            time += g+y + r + ro;
        }
    }


    for (int i = 0; i < (int)activeness.size(); i++)
        if (activeness[i] == n)
        {
            printf("%d\n", i);
            return 0;
        }


    printf("-1\n");
    return 0;
}