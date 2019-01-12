#include <bits/stdc++.h>

using namespace std;

const int MAXN = 1e5 + 1;
int a[MAXN];

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int n;
    cin >> n;
    int k;
    cin >> k;
    int ans = 1e9 + 500;
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
    }
    for (int i = 2; i <= n - 1; ++i) {
        //bigger
        int val = a[i];
        val = max(val, a[i - 1] + k);
        val = max(val, a[i + 1] + k);
        ans = min(ans, val - a[i]);
        //smaller
        val = a[i];
        val = min(val, a[i - 1] - k);
        val = min(val, a[i + 1] - k);
        ans = min(ans, a[i] - val);

    }
    cout << ans << endl;

    return 0;
}