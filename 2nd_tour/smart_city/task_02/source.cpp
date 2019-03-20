#include <stdio.h>

int main() 
{
    int date;
    scanf("%d", &date);
    int part1 = date / 100;
    int part2 = date % 100;

    if (part1 == part2) 
        printf("YES");
    else if (part1 <= 12 && part2 <= 12) 
        printf("NO");
    else
        printf("YES");
}