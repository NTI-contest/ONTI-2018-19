def color_coords(img):    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    
    
    #Бинаризаця
    lower_blue = np.array([0,0,200])
    upper_blue = np.array([180,255,255])
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((11,11),np.uint8)
    mask = cv2.erode(mask,kernel,iterations = 1)
    res = cv2.bitwise_and(img, img, mask= mask)
    res = cv2.GaussianBlur(res,(7,7),0)
    
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    #получение контуров
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE)
    
    centers = []
    clr = ["r","y","g"]
    for cnt in contours:
        #желтый , зеленый, красный
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY= int(M["m01"] / M["m00"])
        #формирование списка центров
        centers.append((cX,cY, hsv[cY, cX][0]))
        
    #Сортировка по значению Hue
    centers = sorted(centers, key = lambda lst: lst[2])
    colors = [(center[0],center[1], color) for center, color in zip(centers, clr)]    
    return colors