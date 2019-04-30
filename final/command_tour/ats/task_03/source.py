def crosses(rgb_frame, noise_frame):
	cross = None
	binary = noise_frame * 255
	border_binary = cv2.rectangle(binary, (0, 0), (binary.shape[1], 
        binary.shape[0]), (0, 0, 0), 5)

	kernel = np.ones((5, 5), np.uint8)
	border_binary = cv2.erode(border_binary, kernel, iterations=1)
	border_binary = cv2.dilate(border_binary, kernel, iterations=2)

	cnts = cv2.findContours(border_binary.copy(), cv2.RETR_EXTERNAL,
                        	cv2.CHAIN_APPROX_NONE)
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
    	epsilon = 0.005 * cv2.arcLength(c, True)
    	approx_c = cv2.approxPolyDP(c, epsilon, True)
    	rect = cv2.minAreaRect(approx_c)
    	box = cv2.boxPoints(rect)
    	box = np.int0(box)
    	x1, y1, w1, h1 = cv2.boundingRect(box)
    	print(h1/w1)
    	if h1 / w1 < 1.5:
        	area = cv2.contourArea(approx_c)
        	if area > 3000:
            	cross = True
            	cv2.drawContours(border_binary, [approx_c], -1, 0, -1)
            	cv2.drawContours(border_binary, [approx_c], 0, 0, len(approx_c))
    	else:
        	cross = False
	clear_frame = border_binary
	return clear_frame, cross


if angle == 0:
    	cross_flag = True
    	first_cross_flag = True

	if not cross_flag:

    	# Управление рулем
    	pi.set_servo_pulsewidth(STEER, int(16.6666666 * angle))

    	# Получение скорости
    	delta_time = delta_time + time.time() - start_time

    	if delta_time > 0.1:
        	speed.update_speed(speed.get_count, delta_time)
        	current_speed = speed.get_speed
        	speed.count_to_zero()
        	delta_time = 0


    	if current_speed < 0.8:
        	if car_speed < 1550:
            	car_speed += 2
    	elif (current_speed > 1.):
        	if car_speed > 1530:
            	car_speed -= 2

    	# print(current_speed, car_speed)

    	pi.set_servo_pulsewidth(ESC, int(car_speed))

	else:
    	if first_cross_flag:
        	# Мы на перекрестке. Останавливаемся и думаем

        	pi.set_servo_pulsewidth(STEER, int(16.6666666 * 90))
        	pi.set_servo_pulsewidth(ESC, 1500)
        	first_cross_flag = False
        	time.sleep(1)


    	# Получаем флаг поворота. Куда повернуть

    	direction = "r"
    	# pi.set_servo_pulsewidth(ESC, 1500)
    	# time.sleep(1)

    	if direction == "r":
    	# Поворачиваем направо
        	pi.set_servo_pulsewidth(STEER, int(16.6666666 * 83))
        	pi.set_servo_pulsewidth(ESC, 1550)
        	time.sleep(1)
        	cross_flag = False

    	if direction == "f":
    	# Едем прямо
        	# Получение скорости
        	delta_time = delta_time + time.time() - start_time

        	if delta_time > 0.1:
            	speed.update_speed(speed.get_count, delta_time)
            	current_speed = speed.get_speed
            	current_distance = current_speed * delta_time
            	distance += current_distance
            	# print(distance)
            	speed.count_to_zero()
            	delta_time = 0


        	if current_speed < 0.8:
            	if car_speed < 1550:
                	car_speed += 2
        	elif (current_speed > 1.):
            	if car_speed > 1530:
                	car_speed -= 2

        	# print(current_speed, car_speed)
        	# pi.set_servo_pulsewidth(ESC, 1550)
        	pi.set_servo_pulsewidth(ESC, int(car_speed))
        	pi.set_servo_pulsewidth(STEER, int(16.6666666 * 94))
        	# заменить время на расстояние

        	print(distance)

        	# time.sleep(5)
        	if distance > 11:
            	cross_flag = False
            	distance = 0

        	print(cross_flag)

    	if direction == "l":
        	# Едем прямо
        	# Получение скорости
        	delta_time = delta_time + time.time() - start_time

        	if delta_time > 0.1:
            	speed.update_speed(speed.get_count, delta_time)
            	current_speed = speed.get_speed
            	current_distance = current_speed * delta_time
            	distance += current_distance
            	# print(distance)
            	speed.count_to_zero()
            	delta_time = 0

        	if current_speed < 0.8:
            	if car_speed < 1550:
                	car_speed += 2
        	elif (current_speed > 1.):
            	if car_speed > 1530:
                	car_speed -= 2

        	# time.sleep(5)
        	if distance <= 5:
            	pi.set_servo_pulsewidth(ESC, int(car_speed))
            	pi.set_servo_pulsewidth(STEER, int(16.6666666 * 95))

        	if distance > 5 and distance < 18:
            	pi.set_servo_pulsewidth(ESC, int(car_speed))
            	pi.set_servo_pulsewidth(STEER, int(16.6666666 * 110))

        	if distance > 18:
            	cross_flag = False
            	distance = 0