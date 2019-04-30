#define _CRT_SECURE_NO_WARNINGS 

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
        std::cin >> arr[y];

    int streets_count = 0;

    for (int i = 1; i < h - 1; i++)
        for (int j = 1; j < w - 1; j++)
        {
            if (arr[i][j] != '#')
                continue;

            bool to_right = arr[i][j - 1] != '#' && arr[i][j + 1] == '#';
            bool to_down =  arr[i - 1][j] != '#' && arr[i + 1][j] == '#';

            streets_count += to_right ? 1 : 0;
            streets_count += to_down ? 1 : 0;
        }


    printf("%d\n", streets_count);
}