#include <cstdio>
#include <string>
#include <cmath>
using namespace std;

FILE *f = nullptr;
FILE *fo = nullptr;

int sol()
{
    int k;
    fscanf(f, "%d", &k);

    int v = 3, c = 1;

    for (;c < k;)
    {
        ++v;
        ++c;
        for (int i = v - 4, lc = 2; i >= 0 && c < k; --i)
        {
            if (c + lc > k)
                break;
            c += lc;
            ++lc;
        }
    }

    fprintf(fo, "%d\n", v);
    return 0;
}

int main()
{
    f = stdin;
    fo = stdout;
    return sol();
}