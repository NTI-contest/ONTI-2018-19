#include <stdio.h> 
#include <vector> 

int main() 
{ 
    int n, m; 
    scanf("%d %d", &n, &m); 
    std::vector<int> times; 
    times.resize(n); 

    times[0] = 0; 
    scanf("%d", &times[1]); 
    for (int i = 2; i < n; i++) { 
        scanf("%d", &times[i]); 
        times[i] += times[i - 1]; 
    } 

    for (int i = 0; i < m; i++) { 
        int a, b; 
        scanf("%d %d", &a, &b); 
        if (a > b) 
            std::swap(a, b); 
        printf("%d\n", times[b - 1] - times[a - 1]); 
    } 
}