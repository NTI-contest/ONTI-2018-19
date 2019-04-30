#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <iostream>
#include <vector>
#include <string>

const int MaxCount = 26;

int main()
{
    int n = 0;
    scanf("%d", &n);

    std::vector<std::vector<char>> table;
    table.resize(MaxCount);
    for (int i = 0; i < MaxCount; i++)
    {
        table[i].resize(MaxCount);
        for (int j = 0; j < MaxCount; j++)
            table[i][j] = 0;
    }

    for (int i = 0; i < n; i++)
    {
        std::string path = "";
        std::cin >> path;

        for (int j = 0; j < (int)path.size() - 1; j++)
        {
            table[path[j] - 'A'][path[j + 1] - 'A'] = 1;
            table[path[j + 1] - 'A'][path[j] - 'A'] = 1;
        }
    }

    int count = 0;
    for (int i = 0; i < MaxCount; i++)
        for (int j = 0; j < MaxCount; j++)
            count += table[i][j];

    count /= 2;
    printf("%d", count);
}