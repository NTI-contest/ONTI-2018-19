#include <iostream>

using namespace std;
typedef long long ll;

const int MAXN = 10000 + 1;
const ll inf = 1e18;
ll r[MAXN], k[MAXN], y[MAXN];

inline ll my_abs(ll x) {
    if (x > 0)
        return x;
    return -x;
}

inline ll cost(int i, int j) {
    return 3 * (r[i] - r[j]) * (r[i] - r[j]) + 2 * my_abs(2 * k[i] - 2 * k[j]) * 
           my_abs(2 * k[i] + 2 * k[j]) + 5 * my_abs(y[i] - y[j]);
}

ll mn[MAXN];
bool used[MAXN];

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int n;
    cin >> n;
    for (int i = 1; i <= n; ++i) {
        cin >> r[i] >> k[i] >> y[i];
        mn[i] = inf;
    }

    ll ans = 0;

    for (int step = 1; step <= n; ++step) {
        int ver = -1;
        for (int i = 1; i <= n; ++i) {
            if (used[i])
                continue;
            if (ver == -1 || mn[i] < mn[ver]) {
                ver = i;
            }
        }
        used[ver] = 1;
        if (step > 1)
            ans += mn[ver];
        for (int j = 1; j <= n; ++j) {
            if (used[j])
                continue;
            mn[j] = min(mn[j], cost(ver, j));
        }

    }
    cout << ans << endl;
    return 0;
}