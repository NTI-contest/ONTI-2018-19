#define _CRT_SECURE_NO_WARNINGS 

#include <string> 
#include <stdio.h> 
#include <cstdio> 
#include <iostream> 
#include <vector> 
#include <queue> 

int GetRoomsCount(float w, float l, float r, float s)
{
    if (w * l * r < s || w * l * (1.0f - r) < s)
        return 1;
    else
        return GetRoomsCount(w * r, l, r, s) + GetRoomsCount(w * (1 - r), l, r, s);
}

int main()
{
    float w = 0;
    float l = 0;
    float r = 0;
    float s = 0;
    scanf("%f %f %f %f", &w, &l, &r, &s);

    int count = GetRoomsCount(w, l, r, s);
    printf("%d", count);
}