n = int(input())

a = list(map(int, input().split()))
a.sort()

sum = 0
hide = []
hide.append(1)
toHide = 0
l = 0
r = 0

while l < n:
    while r < n and a[l] == a[r]:
        r += 1
    sum += (r - l + a[l] - 1) // a[l] * a[l]
    if (r - l + a[l] - 2) // a[l] < (r - l + a[l] - 1) // a[l]:
        toHide = a[l]
    if (r - l + a[l]) // a[l] == (r - l + a[l] - 1) // a[l]:
        hide.append(a[l])
    l = r

hide.reverse()

if toHide == 0:
    if len(hide) == 1 or (a[0] == hide[0] and a[n - 1] == hide[0]):
        sum += 1
elif toHide == 1:
    if len(hide) > 1:
        sum -= 1
    else:
        sum += 1
else:
    for i in hide:
        if i != toHide:
            sum = sum - toHide + (1 if i == 1 else 0)
            break

print(sum)