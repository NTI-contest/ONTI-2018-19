#include <cstdio>
#include <string>
#include <cmath>
#include <cstdint>
#include <algorithm>
using namespace std;

FILE *f, *fo;
char str[100][10001] = {};
int ar[100][10000] = {};

int sol()
{
    int n, m;
    fscanf(f, "%d%d", &n, &m);
    for (int i = 0; i < n; ++i) {
        fscanf(f, "%s", str[i]);
    }
    for (int i = 0; i < n; ++i)
    {
        int z = 0;
        for (int j = 0; j < m; ++j)
            if (str[i][j] == 'a') {
                z = 1;
                break;
            }
        if (!z)
        {
            fprintf(fo, "-1\n");
            return 0;
        }
    }

    for (int i = 0; i < 100; ++i)
        for (int j = 0; j < 10000; ++j)
            ar[i][j] = 12345678;

    for (int i = 0; i < n; ++i)
    {
        int step = 12345678;
        for (int j = 0; j < (m << 1); ++j, ++step)
        {
            if (str[i][j % m] == 'a')
            {
                step = 0;
                ar[i][j % m] = 0;
            } else
            {
                ar[i][j % m] = min(ar[i][j % m], step);
            }
        }

        step = 12345678;
        for (int j = (m << 1) - 1; j >= 0; --j, ++step)
        {
            if (str[i][j % m] == 'a')
            {
                step = 0;
                ar[i][j % m] = 0;
            } else
            {
                ar[i][j % m] = min(ar[i][j % m], step);
            }
        }
    }

    int res = 12345678;
    for (int j = 0; j < m; ++j)
    {
        int q = 0;
        for (int i = 0; i < n; ++i)
            q += ar[i][j];

        res = min(res, q);

    }

    fprintf(fo, "%d\n", res);

    return 0;
}

int main()
{
    f = stdin;
    fo = stdout;
    return sol();
}