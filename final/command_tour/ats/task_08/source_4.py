importrospy
# Загружаем из ноды LED-ленты описание сервиса SetLeds...
fromros_ws281x.srv importSetLeds
# ...и сообщений LEDState и LEDStateArray. Сообщение LEDState
# содержит номер светодиода и его цвет, LEDStateArray - массив
# сообщенийLEDState
fromros_ws281x.msg importLEDState, LEDStateArray
# Для задания цвета используется стандартное сообщение ColorRGBA
fromstd_msgs.msg importColorRGBA
 
# Количество светодиодов в ленте
NUM_LEDS = 60
 
# Прокси к сервису установки состояния светодиодов
set_leds = rospy.ServiceProxy("/led/set_leds", SetLeds, persistent=True)
 
# Вспомогательная функция заполнения всей ленты указанным цветом.
# red, green, blue - интенсивность красного, зелёного, синего цвета
# (задаётсячисломот0 до255)
deffill_strip(red, green, blue):
    # СоздаёмсообщениедляsetLeds
    led_msg = LEDStateArray()
    led_msg.leds = []
    # Для каждого светодиода указываем его новое состояние
    fori inrange(NUM_LEDS):
        led = LEDState(i, ColorRGBA(red, green, blue, 0))
        # Записываем состояние светодиода в сообщение
        led_msg.leds.append(led)
    # Вызываем сервис. После этого вся лента должна стать указанного цвета
   set_leds(led_msg)
# Заполняем ленту разными цветами
fill_strip(255, 0, 0)
rospy.sleep(2.0)
fill_strip(0, 255, 0)
rospy.sleep(2.0)
fill_strip(0, 0, 255)
rospy.sleep(2.0)
# Выключение ленты
fill_strip(0, 0, 0)