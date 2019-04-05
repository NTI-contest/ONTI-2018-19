data = list(map(float, input().split()))
i = 0                    
last_index = 0
while i < len(data) - 20:
    chunk = data[i:i+20]
    if chunk[10]-chunk[0] > 0.3 and chunk[10]-chunk[-1] > 0.3:
        current_index = i + chunk.index(max(chunk)) 
        if last_index == 0:
            last_index = current_index
        else:
            print((current_index - last_index) * 2, end = ' ')
            last_index = current_index
        i += 150
    else:
        i += 1
