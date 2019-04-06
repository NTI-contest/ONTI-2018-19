#include <OrbicraftBus.h> // подключаем библиотеку для работы с конструктором ОрбиКрафт
 
/*
  * Объявим переменную msg как тип данных Message
  * Message - представляет собой структуру, содержащую идентификаторы и данные передаваемого сообщения
*/
Message msg;
 
/*
  * Объявим переменную bus как тип данных OrbicraftBus 
  * OrbicraftBus - представляет собой класс, описывающий взаимодействие Arduino и шины конструктора Orbicraft
*/
OrbicraftBus bus;
 
// Объявим переменную msgSize, в которую будет записываться размер принятого сообщения
uint16_t msgSize = 0;
 
void setup() {
  Serial.begin(9600); // задаем скорость обмена информацией по Serial
}
 
void loop() {
  msgSize = bus.takeMessage(msg); // пробуем прочитать сообщение с помощью метода takeMessage
  Serial.println(msgSize);
  delay(1000);
}


void serialEvent2(){
  bus.serialEventProcess();
}