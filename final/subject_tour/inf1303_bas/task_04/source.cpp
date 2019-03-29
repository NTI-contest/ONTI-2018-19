#include <iostream>

using namespace std;

void solve() {
    int m;
    cin >> m;
    int cnt = 0;
    while(m % 2 == 0){
        m /= 2;
        cnt += 1;
    }
    for(int i = 3; i * i <= m; i += 2){
        while(m % i == 0){
            m /= i;
            cnt += 1;
        }
    }
    if(m != 1){
        cnt += 1;
    }
    if(cnt == 2){
        cout << "YES\n";
    }else{
        cout << "NO\n";
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int tests;
    cin >> tests;
    for(int test = 1; test <= tests; ++test){
        solve();
    }
}