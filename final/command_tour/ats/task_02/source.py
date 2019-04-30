# ищем контуры
countours = cv2.findContours(warped, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
countours = countours[1]
out_img_visual = out_img.copy()

if countours:  # если найден хоть один контур, сортируем их по площади
    countours = sorted(countours, key=cv2.contourArea, reverse=True)
    countour = countours[1]
    Area=cv2.contourArea(count)
    if Area>600:
        rect = cv2.minAreaRect(count)
        width=rect[1][0]
        height=rect[1][1]
        if k>6:
            # останавливаем автомобиль
            control(pi,ESC, 1500, STEER, 90)