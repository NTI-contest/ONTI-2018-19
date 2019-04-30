#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string>
#include <algorithm>

int main()
{
    int a = 0;
    int b = 0;
    scanf("%d %d", &a, &b);
    int c = a * b;

    std::string s_a = std::to_string(a);
    std::string s_b = std::to_string(b);
    std::string s_c = std::to_string(c);

    int line_len = std::max(std::max(s_a.size(), s_b.size()) + 1, s_c.size());

    for (int i = 0; i < line_len - (s_a.size()); i++)
        printf(" ");
    printf("%d\n*", a);
    for (int i = 0; i < line_len - s_b.size() - 1; i++)
        printf(" ");
    printf("%d\n", b);
    for (int i = 0; i < line_len; i++)
        printf("-");
    printf("\n");

    for (int n = 0; n < s_b.size(); n++)
    {
        int cur_mult = a * (s_b[s_b.size() - 1 - n] - '0');
        int cur_mult_len = std::to_string(cur_mult).size();
        for (int i = 0; i < line_len - cur_mult_len - n; i++)
            printf(" ");
        printf("%d", cur_mult);
        for (int i = 0; i < n; i++)
            printf(" ");
        printf("\n");
    }
    for (int i = 0; i < line_len; i++)
        printf("-");
    printf("\n");
    for (int i = 0; i < line_len - s_c.size(); i++)
        printf(" ");
    printf("%d", c);
}