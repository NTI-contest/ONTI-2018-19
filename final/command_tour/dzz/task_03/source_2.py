def control():
    num = 1
    print "Reset magnetometer #%d" % num
    magnetometer_request_reset(num)
    sleep(1)
    print "Enable magnetometer #%d" % num
    magnetometer_turn_on(num)
    print "Get RAW data from magnetometer #%d" % num
    for i in range(0,10):
        (ret, x, y, z) = magnetometer_request_raw(num)
        if ret==0:
            print '[%d] (x, y, z) = %d %d %d' % (i+1, x, y, z)
        else:
            print '[%d] Fail!' % (i+1)
        sleep(1)
    print "Disable magnetometer #%d" % num
    magnetometer_turn_off(num)
    pass