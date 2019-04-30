#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <vector>

static const int table[][10] =
{
    //0  1  2  3  4  5  6  7  8  9
    { 0, 7, 3, 3, 5, 3, 2, 5, 1, 2 }, // 0
    { 7, 0, 8, 6, 4, 8, 9, 2, 8, 7 }, // 1
    { 3, 8, 0, 2, 6, 4, 3, 6, 2, 3 }, // 2
    { 3, 6, 2, 0, 4, 2, 3, 4, 2, 1 }, // 3
    { 5, 4, 6, 4, 0, 4, 5, 4, 4, 3 }, // 4
    { 3, 8, 4, 2, 4, 0, 1, 6, 2, 1 }, // 5
    { 2, 9, 3, 3, 5, 1, 0, 7, 1, 2 }, // 6
    { 5, 2, 6, 4, 4, 6, 7, 0, 6, 5 }, // 7
    { 1, 8, 2, 2, 4, 2, 1, 6, 0, 1 }, // 8
    { 2, 7, 3, 1, 3, 1, 2, 5, 1, 0 }  // 9
};

int main()
{
    int time = 0;
    scanf("%d", &time);
    int hours = time / 100;
    int minutes = time % 100;

    minutes++;
    if (minutes == 60)
    {
        minutes = 0;
        hours++;
    }
    if (hours == 24)
        hours = 0;

    int time2 = hours * 100 + minutes;

    std::vector<int> before{ time / 1000, (time % 1000) / 100, (time % 100) / 10 , (time % 10) };
    std::vector<int> after{ time2 / 1000, (time2 % 1000) / 100, (time2 % 100) / 10 , (time2 % 10) };

    int sum = 0;
    for (int i = 0; i < 4; i++)
        sum += table[before[i]][after[i]];

    printf("%d", sum);
}