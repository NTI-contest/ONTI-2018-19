import math
 
kd = 200			# К-т дифференциальной обратной связи. Если угловая скорость спутника положительна, то спутник надо раскручивать по часовой стрелки, т.е. маховик надо разгонять по часовой стрелке.
kp = -50			# К-т пропорциональной обратной связи. Если текущий угол больше целевого, то спутник надо вращать против часовой стрелки, соответственно маховик надо разгонять против часовой стрелки.
time_step = 0.05		# Временной шаг работы
 
mtr_num = 1			# Номер маховика
hyr_num = 1			# Номер ДУС
mag_num = 1			# Номер магнитометра
 
def mag_calibrated(magx,magy,magz):
	magx_cal = 1.06*(magx + -7.49) + -0.01*(magy + -23.59) + 0.07*(magz + -108.24)
	magy_cal = -0.01*(magx + -7.49) + 1.11*(magy + -23.59) + 0.09*(magz + -108.24)
	magz_cal = 0.07*(magx + -7.49) + 0.09*(magy + -23.59) + 1.00*(magz + -108.24)
	return magx_cal, magy_cal, magz_cal

def angle_transformation(alpha, alpha_goal):
	if alpha<=(alpha_goal - 180):
		alpha = alpha + 360
	elif alpha>(alpha_goal +180):
		alpha = alpha - 360
	return alpha
 
def motor_new_speed_PD(mtr_speed, alpha, alpha_goal, omega, omega_goal):
	mtr_new_speed = int(mtr_speed + kp*(alpha-alpha_goal) + kd*(omega-omega_goal))
	return mtr_new_speed
	# return 0
 
def initialize_all(): # Функция инициализации всех систем
	print "Enable motor №", mtr_num 
	motor_turn_on(mtr_num)
	sleep(1)
 
	print "Enable angular velocity sensor №", hyr_num 
	hyro_turn_on(hyr_num) # Включаем ДУС
	sleep(1)
 
	print "Enable magnetometer", mag_num
	magnetometer_turn_on(mag_num)
	sleep(1)
 
def switch_off_all(): 
	print "Finishing..."
	print "Disable angular velocity sensor №", hyr_num
	hyro_turn_off(hyr_num)   # Выключаем ДУС
	print "Disable magnetometer", mag_num
	magnetometer_turn_off(mag_num)
	motor_set_speed(mtr_num, 0)
	sleep (1)
	motor_turn_off(mtr_num)
	print "Finish program"
 
def control(): 
	initialize_all()
	mtr_state = 0		# Инициализируем статус маховика
	hyro_state = 0 		# Инициализируем статус ДУС
	mag_state = 0 		# Инициализируем статус магнитометра
	alpha_goal = 0		# Целевой угол
	omega_goal = 0 		# Целевая угловая скорость
	mag_alpha = 0
 
	for i in range(500):
		# опрос датчиков и маховика
		mag_state, magx_raw, magy_raw, magz_raw = magnetometer_request_raw(mag_num)
		hyro_state, gx_raw, gy_raw, gz_raw = hyro_request_raw(hyr_num) 
		mtr_state, mtr_speed = motor_request_speed(mtr_num)
 
		if not mag_state: # если магнитометр вернул код ошибки 0, т.е. ошибки нет
			magx_cal, magy_cal, magz_cal = mag_calibrated(magx_raw,magy_raw,magz_raw)
			magy_cal = - magy_cal	
			mag_alpha = math.atan2(magy_cal, magx_cal)/math.pi*180
			print "magx_cal =", magx_cal, "magy_cal =", magy_cal, "magz_cal =", magz_cal # Вывод откалиброванных значений магнитометра
			print "mag_alpha atan2= ", mag_alpha
		elif mag_state == 1:
			print "Fail because of access error, check the connection"
		elif mag_state == 2:
			print "Fail because of interface error, check your code"
 
		if not hyro_state: # если ДУС вернул код ошибки 0, т.е. ошибки нет
			gx_degs = gx_raw * 0.00875
			gy_degs = gy_raw * 0.00875
			gz_degs = gz_raw * 0.00875
			omega = gz_degs	# если ДУС установлен осью z вверх, то угловая скорость спутника совпадает с показаниями ДУС по оси z
			print "gx_degs =", gx_degs, "gy_degs =", gy_degs, "gz_degs =", gz_degs # Выводим данные
		elif hyro_state == 1: # если датчик вернул сообщение об ошибке 1
			print "Fail because of access error, check the connection"
		elif hyro_state == 2: # если датчик вернул сообщение об ошибке 2
			print "Fail because of interface error, check your code"
 
		if not mtr_state:	# если маховик вернул код ошибки 0, т.е. ошибки нет
			print "Motor_speed: ", mtr_speed
			mtr_new_speed = motor_new_speed_PD(mtr_speed,mag_alpha,alpha_goal,gz_degs,omega_goal)	# установка новой скорости маховика
			motor_set_speed(mtr_num, mtr_new_speed)
		sleep(time_step)
	switch_off_all()
