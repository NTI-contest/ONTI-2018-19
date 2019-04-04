n, m = [int(i) for i in input().split()]
a = [int(i) for i in input().split()]

sum = sum(a)

if sum == m:
    print("Yes")
elif sum > m:
    print("No")
else:
    sz = max(a)
    prime = [i > 1 for i in range(sz + 1)]
    for i in range(sz + 1):
        if prime[i]:
            j = i * i
            while j <= sz:
                prime[j] = False
                j += i
    for i in range(n):
        if prime[a[i]] and (m - sum) % a[i] == 0:
            print("Yes", i + 1, (m - sum) // a[i] + 1)
            break
    else:
        print("No")
