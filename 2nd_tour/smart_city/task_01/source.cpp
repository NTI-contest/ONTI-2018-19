#include <cstdio>
#include <cstdint>

using namespace std;

uint8_t pic[1080][1920]{};
int w, h;

void print_line(uint8_t *buf)
{
    for (int i = 0; i < w; i++)
        printf("%d ", (int)buf[i]);
    printf("\n");
}

void deinter_line(uint8_t *up, uint8_t *down)
{
    for (int i = 0; i < w; i++)
        printf("%d ", (((int)up[i] + down[i]) >> 1));
    printf("\n");
}

void loop(int y_beg)
{
    for (int y = y_beg; y < h - 2; y += 2) {
        deinter_line(pic[y], pic[y + 2]);
    }
}

int main()
{
    scanf("%d%d", &w, &h);

    for (int y = 0; y < h; y++)
        for (int x = 0; x < w; x++) {
            int t;
            scanf("%d", &t);
            pic[y][x] = t;
        }

    loop(0);
    print_line(pic[h - 2]);

    print_line(pic[1]);
    loop(1);

    return 0;
}