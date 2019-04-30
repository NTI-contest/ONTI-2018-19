#define _CRT_SECURE_NO_WARNINGS 

#include <memory> 
#include <string> 
#include <stdio.h> 
#include <cstdio> 
#include <iostream> 
#include <vector> 
#include <queue> 

int main()
{
    int count_of_incorrect = 0;
    int n = 0;
    scanf("%d", &n);
    int line_count = 1 << n;

    std::vector<int> answers;
    answers.resize(line_count);

    // Read.
    char *line = (char*)malloc(sizeof(char) * 128);
    for (int i = 0; i < line_count; i++)
    {
        int val = 0;
        scanf("%s %d", line, &val);

        int idx = 0;
        int weight = 1;
        for (int j = 0; j < n; j++) 
        {
            idx += (line[n - j - 1] - '0') * weight;
            weight *= 2;
        }
        answers[idx] = val;
    }

    // Check.
    std::vector<int> zero_arr;
    std::vector<int> one_arr;
    zero_arr.resize(line_count / 2);
    one_arr.resize(line_count / 2);

    int step = line_count / 2;
    int loops_count = 1; // 0000 1111 - one loop
    for (int i = 0; i < n; i++)
    {
        // fill
        for (int j = 0; j < loops_count; j++)
        {
            for (int k = j * step; k < (j + 1) * step; k++)
                zero_arr[k] = answers[k + j * step];

            for (int k = (j + 1) * step; k < (j + 2) * step; k++)
                one_arr[k - step] = answers[k + j * step];
        }

        // check
        bool same = true;
        for (int i = 0; i < line_count / 2; i++)
        {
            if (zero_arr[i] != one_arr[i])
            {
                same = false;
                break;
            }
        }

        if (same)
        {
            printf("X%d ", i);
            count_of_incorrect++;
        }

        step /= 2;
        loops_count *= 2;
    }

    if (count_of_incorrect == 0)
        printf("OK");
}