# coding: utf8
 
importrospy
fromclever importsrv
fromstd_srvs.srv importTrigger
 
rospy.init_node('flight')
 
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
 
# Взлет на 1 метр со скоростью 1 метр в секунду
navigate(x=0, y=0, z=1, speed=1, frame_id='body', auto_arm=True)
 
# Ждем 5 секунд
rospy.sleep(5)
 
# Полет на координаты x=3, y=2, z=1 площадки с углом по рысканью 3.14 
# радиан со скоростью 0.5 метров в секунду
navigate(x=3, y=2, z=1, yaw=3.14, speed=0.5, frame_id='aruco_map')
 
# Ждем 5 секунд
rospy.sleep(5)
 
# Посадка
land()
