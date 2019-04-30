#define _CRT_SECURE_NO_WARNINGS 

#include <string> 
#include <stdio.h> 
#include <cstdio> 
#include <iostream> 
#include <vector> 
#include <queue> 
#include <algorithm>

const int prime_numbers[] = { 
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
...
99881, 99901, 99907, 99923, 99929, 99961, 99971, 99989, 99991 
};

int main()
{
    int count = 0;
    scanf("%d", &count);
    for (int c = 0; c < count; c++)
    {

        int n = 0;
        scanf("%d", &n);

        int prime_count = sizeof(prime_numbers) / sizeof(prime_numbers[0]);

        int dividers = 0;
        for (int i = 0; i < prime_count; i++)
        {
            int n_copy = n;
            while (n_copy % prime_numbers[i] == 0)
            {
                n_copy /= prime_numbers[i];
                dividers++;
            }
            if (prime_numbers[i] > n || dividers > 2)
                break;
        }

        if (dividers == 2)
            printf("YES\n");
        else
            printf("NO\n");
    }
}