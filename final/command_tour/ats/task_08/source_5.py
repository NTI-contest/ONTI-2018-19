Y = 0.24
YAW = 1.56
def pick_up():
   navigate(z=1, x=X, y=Y, yaw=YAW, frame_id='aruco_map', speed=0.2)
 
    while True:
       rospy.sleep(0.2)
 
        telem = get_telemetry(frame_id='aruco_map')
 
        if math.isnan(telem.x):
            # don't see marker
           print 'dont see'
           continue
 
        telem.x -= X
        telem.y -= Y
 
        if telem.z < 0.35:
            return
 
        if math.hypot(telem.x, telem.y) < 0.08:
            # inside
           print 'land', telem.z
           set_position(x=X, y=Y, z=telem.z - 0.1, yaw=YAW, frame_id='aruco_map')
        else:
           print 'hor', telem.z
           set_position(x=X, y=Y, z=telem.z, yaw=YAW, frame_id='aruco_map')            
i = 0
while i < 4:
    pick_up()
    print 'repeat'
   navigate(z=0.5, frame_id='body', speed=1)
    rospy.sleep(4)
    i += 1
