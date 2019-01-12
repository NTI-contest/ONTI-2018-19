#include <iostream>
#include <cmath>

#define EPS 1e-9

using namespace std;

int main() {
    double d, r;
    cin >> d >> r;
    double sine = d / 2 / r;
    if (sine > 1)
        cout << -1;
    else {
        double angle = asin(sine);
        cout << (long long) floor(M_PI / angle + EPS);
    }
    return 0;
}