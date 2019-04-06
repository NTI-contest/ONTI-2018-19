def control():
    num = 1
    print "Reset motor #%d" % num
    motor_request_reset(num)
    sleep(1)
    #print "Enable hyro #%d" % num
    motor_turn_on(num)
    #print "Get RAW data from hyro #%d" % num
    (err, speed) = motor_set_speed(num, 3000);
    sleep(15)
    print(err, speed)
    motor_set_speed(num, 0);
    sleep(15);
    (err, speed) = motor_set_speed(num, -3000);
    sleep(5)
    print(err, speed)
    motor_set_speed(num, 0);
    sleep(2);
    motor_turn_off(num);
    pass