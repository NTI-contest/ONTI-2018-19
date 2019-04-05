data = list(map(float, input().split())) 
i = 0                        
beats = 0                    
while i < len(data) - 20:
    chunk = data[i:i+20]
    if chunk[10] - chunk[0] > 0.3 and chunk[10]-chunk[-1] > 0.3: 
        beats += 1  
        i += 150          
    else:
        i += 1
print(beats)
