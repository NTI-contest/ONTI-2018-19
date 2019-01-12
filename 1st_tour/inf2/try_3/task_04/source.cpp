#include <bits/stdc++.h>

using namespace std;
typedef long long ll;
const ll inf_ll = 1e16;
const int MAXN = 1e5 + 100;

ll x[MAXN], y[MAXN];
ll dis[MAXN];

ll dist(int a, int b) {
    return (x[a] - x[b]) * (x[a] - x[b]) + (y[a] - y[b]) * (y[a] - y[b]);
}

bool used[MAXN];

int main() {
    int n;
    cin >> n;
    ll k;
    cin >> k;
    for (int i = 1; i <= n; ++i) {
        cin >> x[i] >> y[i];
    }
    int s, t;
    cin >> s >> t;
    for (int i = 1; i <= n; ++i) {
        dis[i] = inf_ll;
    }
    dis[s] = 0;
    for (int i = 1; i <= n; ++i) {
        int ver = -1;
        for (int e = 1; e <= n; ++e) {
            if (!used[e] && (ver == -1 || dis[e] < dis[ver])) {
                ver = e;
            }
        }

        int v = ver;
        used[v] = 1;
        for (int to = 1; to <= n; ++to) {
            if (dist(v, to) > k)
                continue;
            if (dis[to] > dis[v] + dist(v, to)) {
                dis[to] = dis[v] + dist(v, to);
            }
        }
    }

    if (dis[t] == inf_ll) {
        cout << -1 << endl;
    } else {
        cout << dis[t] << endl;
    }
}