h_w, w_w = map(int, input().split())
windows = [list(map(int, input().split())) for i in range(h_w)]

h_p, w_p = map(int, input().split())
pattern = [list(map(int, input().split())) for i in range(h_p)]

if not any(map(any, pattern)):
    print(1)
else:
    ans = 0
    for y1 in range(h_w - h_p + 1):
        for x1 in range(w_w - w_p + 1):
            this_position_ok = True

            for y2 in range(h_p):
                for x2 in range(w_p):
                    if pattern[y2][x2] == 1 and windows[y1 + y2][x1 + x2] == 0:
                        this_position_ok = False

            ans += this_position_ok
    print(ans)