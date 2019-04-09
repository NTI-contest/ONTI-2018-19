def detect(filename):  
    # код, который находит маркеры
    frame =cv2.imread(filename)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()               
    aruko_paraps = aruco.detectMarkers(gray, aruco_dict, 
                                                          parameters=parameters)  
    
    
    frame =cv2.imread(filename)
    #получение сетки между маркерами
    warped_img = warp_by_4markers(frame, aruko_paraps)
    
    #получение объектов (цветных клеток) на сетке
    objects = get_objects(warped_img)
    
    #подписываем объекты на сетке 
    for obj in objects:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(warped_img, obj[0], obj[1], font, 1,(255,255,255),2,cv2.LINE_AA)
    plt.subplot(121),plt.imshow(warped_img),plt.title('Input')
       
    return objects