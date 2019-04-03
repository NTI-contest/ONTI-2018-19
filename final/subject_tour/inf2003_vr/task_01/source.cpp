#define _CRT_SECURE_NO_WARNINGS
#define _USE_MATH_DEFINES

#pragma comment(linker, "/STACK:66777216")

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <cmath>
#include <stack>
#include <functional>
#include <set>
#include <queue>
#include <string>
#include <map>
#include <iomanip>
#include <sstream>
#include <cassert>

#define sqr(x) ((x)*(x))

using namespace std;

int main()
{
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);

	int R, r, w, x, y, z, v, n;
	cin >> R >> w >> x >> y >> z >> v >> n;

	if (x * x + y * y > R * R)
	{
		cout << 0;
		return 0;
	}

	double t = double(z) / double(v);
	double start_angle = atan2(y, x) + 2 * M_PI - M_PI / 2;
	double total_rotation = (t * w) / 360 * 2 * M_PI + start_angle;
	double cur_sin = sin(total_rotation);
	double cur_cos = cos(total_rotation);
	double cur_angle = atan2(cur_sin, cur_cos);
	if (cur_angle < 0)
		cur_angle += 2 * M_PI;
	double one_sector = 2 * M_PI / n;
	int ind = cur_angle / one_sector;

	cout << n - ind;

}
