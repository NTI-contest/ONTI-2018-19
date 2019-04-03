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

int arr[1000000];
int mark[1000000];

int main()
{
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
	int n, m, k;
	cin >> n >> m >> k;
	int goal = k - n + m + 1;
	int val = k - 2 * n + 2 * m + 1;

	for (int i = 0; i < n; i++)
	{
		cin >> arr[i];
		if (arr[i] <= val && val <= k && val < goal)
		{
			val++;
		}
		else
		{
			mark[i] = 1;
		}
	}
	if (val >= goal)
	{
		cout << "YES" << endl;

		for (int i = 0; i < n; i++)
			if (mark[i])
				cout << "D";
			else
				cout << "U";

		for (int i = n - 1; i >= 0; i--)
			if (mark[i])
				cout << "D";
			else
				cout << "U";
	}
	else
		cout << "NO";
}