import cv2	          #импорт библиотеки OpenCV
import numpy	          #импорт библиотеки NumPy (работа с массивами)
for i in range(1,6):	        
    #цикл по количеству изображений, у нас 5
    Frame = cv2.imread(str(i) + ".jpg")	
    #считываем изображение из файла, у которого имя совпадает с номером, 
    #в переменную Frame
    Frame = cv2.resize(Frame, (40,100))	
    #меняем размер изображения
    cv2.imshow("Traffic Lights " + str(i), Frame)	
    #выводим его в окно ''TrafficLight"
    Cuted_Frame = Frame[4:95, 4:35]	
    #обрезаем края изображения
    cv2.imshow("Cuted Frame " + str(i), Cuted_Frame)	
    #выводим в окно "CutedFrame"
    HSV = cv2.cvtColor(Cuted_Frame, cv2.COLOR_BGR2HSV)	
    #переводим в HSV
    Brightness_Only = HSV[:, :, 2]	
    #оставляем канал яркости
    cv2.imshow("Brightness Only " + str(i), Brightness_Only)	
    #выводим в окно "Brightness Only "
    Red_Sum_Brightness = numpy.sum(Brightness_Only[0:30, 0:30])
    Yellow_Sum_Brightness = numpy.sum(Brightness_Only[31:60, 0:30])
    Green_Sum_Brightness = numpy.sum(Brightness_Only[61:90, 0:30])	
    #суммируем яркости в областях каждого цвета
    cv2.rectangle(Cuted_Frame, (0, 0), (30, 30), (0, 0, 255), 1)
    cv2.rectangle(Cuted_Frame, (0, 31), (30, 60), (0, 255, 255), 1)
    cv2.rectangle(Cuted_Frame, (0, 61), (30, 90), (0, 255, 0), 1)
    #для наглядности обводим каждую область линией своего цвета
    cv2.imshow("Areas " + str(i),Cuted_Frame)	
    #и выводим в окно "Areas"
    print(str(Red_Sum_Brightness) + " : " + str(Yellow_Sum_Brightness) + " : " + 
       str(Green_Sum_Brightness))
    #выводим на печать суммы яркости для всех трёх областей
    if Red_Sum_Brightness>Yellow_Sum_Brightness:
        if Red_Sum_Brightness>Green_Sum_Brightness:
            print('Red')
        else:
            print('Green')
    elif Green_Sum_Brightness>Yellow_Sum_Brightness:
        print('Green')
    else:
        print('Yellow')	
    #определяем для области какого цвета сумма максимальна и выводим на печать цвет
    cv2.moveWindow("Traffic Lights "+str(i),50,50)
    cv2.moveWindow("Cuted Frame "+str(i),350,150)
    cv2.moveWindow("Brightness Only "+ str(i),650,250)
    cv2.moveWindow("Areas "+str(i),950,350)
    #все окна располагаем удобным образом
    if cv2.waitKey() == 27:
        break	
    #нажата кнопка "Esc"?
    #тогда выход из цикла,
    #нет – следующий кадр
cv2.destroyAllWindows()	
#закрываем все окна