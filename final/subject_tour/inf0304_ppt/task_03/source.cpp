#define _CRT_SECURE_NO_WARNINGS 

#include <stdio.h>
#include <cmath>
#include <math.h>
#include <algorithm>
#include <cstdlib>
#include <vector>

using namespace std;

struct point
{
    float x = 0;
    float y = 0;
};

float square(const std::vector<point> &fig)
{
    float res = 0;
    for (int i = 0; i < fig.size(); i++)
    {
        point
            p1 = i ? fig[i - 1] : fig.back(),
            p2 = fig[i];
        res += (p1.x - p2.x) * (p1.y + p2.y);
    }
    return fabs(res) / 2;
}

int main()
{
    int n = 0;
    float square_per_parking = 0;
    scanf("%d %f", &n, &square_per_parking);

    int parkings_count = 0;
    std::vector<float> district_squares;
    district_squares.resize(n);
    for (int i = 0; i < n; i++)
    {
        int point_count = 0;
        scanf("%d", &point_count);
        std::vector<point> fig;
        fig.resize(point_count);

        for (int j = 0; j < point_count; j++)
            scanf("%f %f", &fig[j].x, &fig[j].y);

        district_squares[i] = square(fig);
        parkings_count += (int)::ceilf(district_squares[i] / square_per_parking);
    }

    printf("%d", parkings_count);
}