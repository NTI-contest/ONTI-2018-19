def solve():
    res = 0
    while True:
        cmd = input().split()
        if cmd[0] in ['END', 'BLE']:
            break
        elif cmd[0] == 'BLB':
            continue
        elif cmd[0] == 'MOV':
            res += int(cmd[1])
        else:
            res += int(cmd[1]) * solve()
    return res

print(solve())