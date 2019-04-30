import paho.mqtt.client asmqtt  # Импортирование библиотеки mqtt
# Callback, вызываемый при получении от сервера подтверждения о подключении
defon_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Если подписываться на топик в on_connect, то при обрыве соединения
    # и повторном подключении произойдёт автоматическое переподписание
   client.subscribe("/xxx")
# Callback, вызываемый при появлении сообщения в одном из топиков, на который
# подписанклиент
defon_message(client, userdata, msg):
    # В объекте msg хранится топик, в который пришло сообщение (в поле topic)
    # и само сообщение (в поле payload)
    print(msg.topic, str(msg.payload))
# Инициализация клиента MQTT
client = mqtt.Client()
# Здесь указываются callback'и, вызываемые при подключении и получении сообщения
client.on_connect = on_connect
client.on_message = on_message
# Подключение к MQTT-брокеру. Первый параметр - имя или адрес брокера, второй - порт
# (по умолчанию 1883), третий - максимальное время между сообщениями в секундах
# (по умолчанию 60).
client.connect('192.168.1.199', 1883, 60)
# Метод loop_start создаёт поток, в котором будет производиться опрос сервера и
# вызов callback'ов.
client.loop_start()
# Далее продолжается ваша программа
