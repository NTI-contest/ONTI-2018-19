#include <Servo.h>

// Стандартные значения ШИМ
const uint16_t PWM_MIN = 1000;
const uint16_t PWM_MAX = 2000;
const uint16_t PWM_AVG = 1500;

// ШИМ запуска двигателя
const uint16_t PWM_ENG_START = 1200;

// Максимальный ШИМ для двигателя (ШИМ на максимально разрешенной тяге)
const uint16_t PWM_ENG_MAX = 1500;

// Коэффициент нарастания ШИМ (тяга) [ШИМ/сек]
const float k = 150;

// Стандартное время работы (мс)
const uint16_t OPTIME = 3000;

// ШИМ каналы
Servo AIL;  // элероны
Servo ELE;  // руль высоты
Servo THR;  // тяга двигателя
Servo RUD;  // руль направления


void setup() 
{
  //============================================================================
  // Порт для оталадки
  Serial.begin(115200); while(!Serial) { ; }

  // подключение каналов управления
  AIL.attach(2);  AIL.write(PWM_AVG);
  ELE.attach(3);  ELE.write(PWM_AVG);
  THR.attach(5);  THR.write(PWM_MIN); 
  RUD.attach(6);  RUD.write(PWM_AVG);
  
  
  //============================================================================
  // 1. Двигатель

  // Подкинуть ШИМ до стартового
  THR.writeMicroseconds(PWM_ENG_START);

  // Во ибежание несчастных случаев на производстве ШИМ изменять линейно
  uint32_t tstart = millis();
  uint16_t pwm = 0;

  pwm = PWM_ENG_START + k*float(millis()  - tstart)/1000.0; 
  while (millis()  - tstart < OPTIME)
  {
    // Ограничение ШИМ 
    if (pwm < PWM_ENG_MAX) 
    {
      pwm = PWM_ENG_MAX;
    }
    
    THR.writeMicroseconds(pwm);

    // 20 Hz
    delay(50);
  }
  THR.writeMicroseconds(PWM_MIN);
  delay(1000); //задержка между выключением двигателя и подачей сигналов 
  // на органы управления
  //============================================================================
  // 2. Органы управления
  
  //----------------------------------------------------------------------------
  // 2.1. Руль высоты
  Serial.print("ELE UP\n");
  ELE.writeMicroseconds(PWM_MAX);
  delay(OPTIME);

  Serial.print("ELE DOWN\n");
  ELE.writeMicroseconds(PWM_MIN);
  delay(OPTIME);

  Serial.print("ELE CENTER\n\n");
  ELE.writeMicroseconds(PWM_AVG);
  delay(OPTIME);

  //----------------------------------------------------------------------------
  // 2.2. Руль направления
  Serial.print("RUD UP\n");
  RUD.writeMicroseconds(PWM_MAX);
  delay(OPTIME);

  Serial.print("RUD DOWN\n");
  RUD.writeMicroseconds(PWM_MIN);
  delay(OPTIME);

  Serial.print("RUD CENTER\n\n");
  RUD.writeMicroseconds(PWM_AVG);
  delay(OPTIME);

  //----------------------------------------------------------------------------
  // 2.3. Элероны
  Serial.print("AIL UP\n");
  AIL.writeMicroseconds(PWM_MAX);
  delay(OPTIME);

  Serial.print("AIL DOWN\n");
  AIL.writeMicroseconds(PWM_MIN);
  delay(OPTIME);

  Serial.print("AIL CENTER\n\n");
  AIL.writeMicroseconds(PWM_AVG);
  delay(OPTIME);
  
}

void loop() 
{
  // пустой цикл
}
