h, n = map(int, input().split())
queries = list(map(int, input().split()))
total_time = h * 60

queries.sort()

cur_sum = 0
ans = 0
for q in queries:
    cur_sum += q
    ans += 1

    if cur_sum > total_time:
        ans -= 1
        break

print(ans)
