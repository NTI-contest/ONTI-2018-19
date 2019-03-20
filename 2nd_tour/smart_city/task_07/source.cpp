#include <string>
#include <stdio.h>
#include <cstdio>
#include <iostream>
#include <vector>
#include <queue>

int main()
{
    int w;
    int h;
    scanf("%d %d", &w, &h);

    std::vector<std::string> arr;
    arr.resize(h);
    for (int y = 0; y < h; y++)
    {
        std::cin >> arr[y];
    }

    bool was_added = true;
    int painted = 1; // petr itself.
    while (was_added)
    {
        was_added = false;

        for (int y = 1; y < h - 1; y++)
            for (int x = 1; x < w - 1; x++)
            {
                if ((arr[y][x] == '.') &&
                    (arr[y - 1][x] == '@' ||
                    arr[y + 1][x] == '@' ||
                    arr[y][x - 1] == '@' ||
                    arr[y][x + 1] == '@')) 
                {
                    arr[y][x] = '@';
                    was_added = true;
                    painted++;
                }
            }
    }

    printf("%d\n", painted);
}