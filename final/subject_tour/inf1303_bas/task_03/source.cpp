#define _CRT_SECURE_NO_WARNINGS 

#include <stdio.h>
#include <vector>
#include <string>
#include <iostream>
#include <cstdio>
#include <algorithm>

unsigned long long EncodeNumber(std::string &number)
{
    unsigned long long code = (unsigned long long)number[0];
    code += (unsigned long long)number[1] << 8;
    code += (unsigned long long)number[2] << 16;
    code += (unsigned long long)number[3] << 24;
    code += (unsigned long long)number[4] << 32;
    code += (unsigned long long)number[5] << 40;
    code += (unsigned long long)number[6] << 48;
    code += (unsigned long long)number[7] << 56;
    return code;
}

bool binarySearch(std::vector<unsigned long long> &data, unsigned long long value)
{
    int l = 0;
    int r = data.size() - 1;
    while (l <= r)
    {
        unsigned long long m = l + (r - l) / 2;
        if (data[m] == value)
            return true;
        if (data[m] < value)
            l = m + 1;
        else
            r = m - 1;
    }
    return false;
}

int main()
{
    int n;
    int m;
    scanf("%d %d", &n, &m);

    std::vector<unsigned long long> database;
    database.resize(n);

    for (int i = 0; i < n; i++)
    {
        std::string number;
        std::cin >> number;
        database[i] = EncodeNumber(number);
    }

    std::sort(database.begin(), database.end());

    for (int i = 0; i < m; i++)
    {
        std::string number;
        std::cin >> number;
        unsigned long long code = EncodeNumber(number);
        if (binarySearch(database, code))
            printf("YES\n");
        else
            printf("NO\n");
    }

    return 0;
}