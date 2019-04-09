import json
import math

[a, b, c, x] = list(map(lambda x : x['faceLandmarks'], json.loads(input())))

keys = ['eyeLeftInner','eyeRightInner','noseRootLeft', 'noseRootRight', 'eyeLeftTop',
        'eyeLeftBottom', 'eyeRightTop', 'eyeRightBottom', 'mouthRight', 'mouthLeft', 
        'eyeLeftOuter', 'eyeRightOuter', 'eyebrowLeftOuter', 'eyebrowRightOuter',    
        'eyebrowLeftInner', 'eyebrowRightInner']                                      
                                                                                      
                                                                                      
def check(a, x):                                                                        
    length = 0                                                                           
    unit1 = (a['eyeLeftInner']['x'] - a['eyeRightInner']['x']) ** 2 + (                
                a['eyeLeftInner']['y'] - a['eyeRightInner']['y']) ** 2                  
    unit2 = (x['eyeLeftInner']['x'] - x['eyeRightInner']['x']) ** 2 + (                 
                x['eyeLeftInner']['y'] - x['eyeRightInner']['y']) ** 2                    
    for key in keys:
        for keyx in keys:
            length += (math.sqrt(((a[key]['x'] - a[keyx]['x']) ** 2 +
                                  (a[key]['y'] - a[keyx]['y']) ** 2) / unit1)
                       - math.sqrt(((x[key]['x'] - x[keyx]['x']) ** 2 +
                                    (x[key]['y'] - x[keyx]['y']) ** 2) / unit2)) ** 2

    return length


ax, bx, cx = check(a, x), check(b, x), check(c, x)

if ax < bx and ax < cx:
    print(0)
elif bx < cx:
    print(1)
else:
    print(2)