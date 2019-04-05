def control():
    num = 1
    print "Reset hyro #%d" % num
    hyro_request_reset(num)
    sleep(1)
    print "Enable hyro #%d" % num
    hyro_turn_on(num)
    sleep(2)
    print "Get RAW data from hyro #%d" % num
    for i in range(0,10):
        (ret, x, y, z) = hyro_request_raw(num)
        if ret==0:
            print '[%d] (x, y, z) = %d %d %d' % (i+1, x, y, z)
        else:
            print '[%d] Fail!' % (i+1)
        sleep(1)
    print "Disable hyro #%d" % num
    hyro_turn_off(num)
    pass