def control(): 
    hyro_turn_on(1) 
    motor_turn_on(1) 
    sleep(1) 
    kp=1 
    kd=12 
    motor_speed = 0 
    speed_hyro_old = 0 
    for i in range(300): 
        # снимаем показания с датчика угловой скорости и берём значение 
        # по оси z
        speed_hyro_new = hyro_request_raw(1)[3] 
        # вычисляем значение скорости на маховик через изменение угловой 
        # скорости и предыдущее значение скорости маховика
        motor_speed = kp*motor_speed - kd*(speed_hyro_new - speed_hyro_old) 
        #sleep(3) 
        # пишем ограничение скорости на маховик
        if motor_speed > 4000: 
            motor_speed = 4000 
        if motor_speed < -4000: 
            motor_speed = -4000 
        # устанавливаем вычисленную скорость на маховик, 
        # предварительно округлив её до целого
        motor_set_speed(1, int(motor_speed_new)) 
        sleep(1) 
        # выводим в веб-консоль полученные значения
        print('Угловая скорость: %d') % speed_hyro_new 
        print('Скорость маховика: %d') % motor_speed
    motor_set_speed(1, 0) 
    motor_turn_off(1) 
    hyro_turn_off(1)