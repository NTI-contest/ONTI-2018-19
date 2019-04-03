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

int mp[101][101];
int pref_sum[101][101];

int calc_sum(int y1, int x1, int y2, int x2)
{
	int res = pref_sum[y2][x2];
	res += pref_sum[y1 - 1][x1 - 1];
	res -= pref_sum[y1 - 1][x2];
	res -= pref_sum[y2][x1 - 1];
	return res;
}

int main()
{
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
	int W, H, N;
	cin >> W >> H >> N;

	for (int i = 1; i <= H; i++)
	{
		int row_sum = 0;
		for (int j = 1; j <= W; j++)
		{
			char val;
			cin >> val;
			if (val == '#')
				mp[i][j] = 1;
			row_sum += mp[i][j];
			pref_sum[i][j] = row_sum;
			pref_sum[i][j] += pref_sum[i - 1][j];
		}
	}
	int ans = 0;

	for (int i = 1; i <= H; i++)
		for (int j = 1; j <= W; j++)
			for (int ii = i; ii <= H; ii++)
				for (int jj = j; jj <= W; jj++)
				{
					int sum_center = calc_sum(i, j, ii, jj);
					int res = (ii - i + 1) * (jj - j + 1) - sum_center;
					int res_outside = calc_sum(1, 1, H, W) - sum_center;
					res += res_outside;
					if (res <= N)
						ans++;
				}

	cout << ans;
}