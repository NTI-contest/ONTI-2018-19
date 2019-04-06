// Напишите программу управления ШИМ сигналом через потенциометр. 
// Длительность импульса ШИМ сигнала должна изменяться от 1000 до 2000 мкс 
// в зависимости от напряжения на выходе потенциометра (1000 мкс для 
// минимального выходного напряжения и 2000 мкс для максимального). 
// Соберите схему и при помощи осциллографа снимите статическую характеристику 
// напряжение-длительность импульса ШИМ сигнала.

#include <math.h>
#include <Servo.h>

// Аналоговая ножка для приема сигнала с потенциометра
const uint8_t VRPIN = A0;

// Отсчеты АЦП (0 - 1023)
uint16_t adcCounts = 0;

// Цифровая ШИМ ножка
const uint8_t SRVPIN = 2;

// Цифровой ШИМ выход
Servo CTRL;

// Выходное значение (1000 - 2000 мкс)
uint16_t pwmCounts = 0;

// Коэффициенты линейной зависимости пересчета отсчеты АЦП - ШИМ
float k = 0;
float b = 0;

// Максимальное и минимальное значение напряжений с потенциометра
// Установлены такие значения, что они гарантированно перезапишутся при 
// их экспериментальном определении
uint16_t adcCounts_min = 1024;
uint16_t adcCounts_max = 0;

void setup() 
{
  // Настройка портов ввода-вывода
  Serial.begin(115200); while(!Serial) { ; }
  pinMode(VRPIN,INPUT);
  CTRL.attach(SRVPIN);
  
  // Определение минимального и максимального значений
  Serial.print("Rotate potentiometer/n");

  uint32_t startTime = millis();
  while (millis() - startTime < 5000)
  {
    adcCounts = analogRead(VRPIN);
    if (adcCounts < adcCounts_min) adcCounts_min = adcCounts;
    if (adcCounts > adcCounts_max) adcCounts_max = adcCounts;
  }

  Serial.print("adcCounts_min = " + String(adcCounts_min) + "\n");
  Serial.print("adcCounts_max = " + String(adcCounts_max) + "\n");

  // Расчет коэффициентов преобразования
  k = 1000.0 / float(adcCounts_max - adcCounts_min);
  b = 1000.0 * (1.0 - float(adcCounts_min) / float(adcCounts_max - adcCounts_min));
}

void loop() 
{
  // Чтение входного напряжения
  adcCounts = analogRead(VRPIN);
  
  // Расчет выходного ШИМ
  pwmCounts = round(k* float(adcCounts) + b);
  
  // Ограничение ШИМ на случай погрешностей округления
  if (pwmCounts < 1000) pwmCounts = 1000;
  if (pwmCounts > 2000) pwmCounts = 2000;

  // Вывод ШИМ
  CTRL.writeMicroseconds(pwmCounts);

  // Для отладки
  Serial.print("adcCounts = " + String(adcCounts) + "\n");
  Serial.print("pwmCounts = " + String(pwmCounts) + "\n");

  // 20 Гц
  delay(50);
}
