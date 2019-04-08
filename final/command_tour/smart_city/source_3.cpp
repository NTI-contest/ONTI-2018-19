// Моторы подключаются к клеммам M1+,M1-,M2+,M2-  
// Motor shield использует четыре контакта 6,5,7,4 для управления моторами 
#define SPEED_LEFT       6
#define SPEED_RIGHT      5
#define DIR_LEFT         4
#define DIR_RIGHT        7
#define LEFT_SENSOR_PIN  2
#define RIGHT_SENSOR_PIN 3
 
// Скорость, с которой мы движемся вперёд (0-255)
#define SPEED            40
 
// Скорость прохождения сложных участков
#define SLOW_SPEED       30
 
#define BACK_SLOW_SPEED  30
#define BACK_FAST_SPEED  50
 
// Коэффициент, задающий во сколько раз нужно затормозить
// одно из колёс для поворота
#define BRAKE_K          4
 
#define STATE_FORWARD    0
#define STATE_RIGHT      1
#define STATE_LEFT       2
 
#define SPEED_STEP       2
 
#define FAST_TIME_THRESHOLD     10
 
int state = STATE_FORWARD;
int currentSpeed = SPEED;
unsigned long fastTime = 0;
 
void runForward() 
{
    state = STATE_FORWARD;
 
    fastTime += 1;
    if (/*millis() - */fastTime < FAST_TIME_THRESHOLD) {
        currentSpeed = SLOW_SPEED;
    } else {
        currentSpeed = min(currentSpeed + SPEED_STEP, SPEED);
    }

//    Serial.println(currentSpeed);
 
    analogWrite(SPEED_LEFT, currentSpeed);
    analogWrite(SPEED_RIGHT, currentSpeed + 5);
 
    digitalWrite(DIR_LEFT, HIGH);
    digitalWrite(DIR_RIGHT, HIGH);
}
 
void steerRight() 
{
    state = STATE_RIGHT;
    fastTime = /*millis()*/0;
 
    // Замедляем правое колесо относительно левого,
    // чтобы начать поворот
    analogWrite(SPEED_RIGHT, 0);
    analogWrite(SPEED_LEFT, SPEED);
 
    digitalWrite(DIR_LEFT, HIGH);
    digitalWrite(DIR_RIGHT, HIGH);
}
 
void steerLeft() 
{
    state = STATE_LEFT;
    fastTime = /*millis()*/0;
 
    analogWrite(SPEED_LEFT, 0);
    analogWrite(SPEED_RIGHT, SPEED + 5);
 
    digitalWrite(DIR_LEFT, HIGH);
    digitalWrite(DIR_RIGHT, HIGH);
}
 
 
void stepBack(int duration, int state) {
    if (!duration)
        return;
 
    // В зависимости от направления поворота при движении назад будем
    // делать небольшой разворот 
    int leftSpeed = (state == STATE_RIGHT) ? BACK_SLOW_SPEED : BACK_FAST_SPEED;
    int rightSpeed = (state == STATE_LEFT) ? BACK_SLOW_SPEED : BACK_FAST_SPEED;
 
    analogWrite(SPEED_LEFT, leftSpeed);
    analogWrite(SPEED_RIGHT, rightSpeed + 5);
 
    // реверс колёс
    digitalWrite(DIR_RIGHT, LOW);
    digitalWrite(DIR_LEFT, LOW);
 
    delay(duration);
}


typedef enum {
  START,
  TRAFFIC_LIGHTS_1,
  CROSSROAD_1,
  LABLE_ZKH,
  LABLE_HOUSE,
  LABLE_CHILD,
  CROSSROAD_2,
  CROSSROAD_3,
  TRAFFIC_LIGHTS_2,
  END
} lable_t;

char *lable_name[] = {
  "START",
  "TRAFFIC_LIGHTS_1",
  "CROSSROAD_1",
  "LABLE_ZKH",
  "LABLE_HOUSE",
  "LABLE_CHILD",
  "CROSSROAD_2",
  "CROSSROAD_3",
  "TRAFFIC_LIGHTS_2",
  "END"
};

char buff[32] = {0};
static byte lable_cnt = START;
static bool on_lable = false;
static unsigned long lable_millis = 0;
 
void setup() 
{
  Serial.begin(115200);
  
  radio_begin();
  
  // Настраивает выводы платы 4,5,6,7 на вывод сигналов 
  for(int i = 4; i <= 7; i++) {
    pinMode(i, OUTPUT);
  }

//  sprintf(buff, "station: %d", lable_cnt);
//  radio_write(buff, strlen(buff));
//  delay(200);

  do {
    int len = radio_read(buff, 10);
    if (len && strstr(buff, "taxi")) {
      break;
    }
  } while(1);

  // Едем вперёд
  runForward();
}
 
void loop() 
{
  int len = 0;

  if (lable_cnt == START) {
    len = radio_read(buff, 10);
  }

  // Наш робот ездит по белому полю с чёрным треком. В обратном случае не нужно
  // инвертировать значения с датчиков
  boolean left = !digitalRead(LEFT_SENSOR_PIN);
  boolean right = !digitalRead(RIGHT_SENSOR_PIN);

  if ( (left == right) && (left == false) ) {
    if (!on_lable) {
      on_lable = true;
      lable_cnt++;

      char buf[16];
      sprintf(buf, "station: %d", lable_cnt);
      radio_write(buf, strlen(buf));

      switch (lable_cnt) {
        case TRAFFIC_LIGHTS_1:
          if (strstr(buff, "color:red")) {
            analogWrite(SPEED_LEFT, 0);
            analogWrite(SPEED_RIGHT, 0);

            do {
              delay(50);
              len = radio_read(buff, 10);
              if (len && strstr(buff, "color:green")) {
                break;
              }
            } while(1);
          }
        break;

        case CROSSROAD_1:
        case CROSSROAD_2:
        case TRAFFIC_LIGHTS_2:
          // Проезжаем
//          delay(50);
        break;

        case LABLE_ZKH:
        case LABLE_HOUSE:
        case LABLE_CHILD:
          analogWrite(SPEED_LEFT, 0);
          analogWrite(SPEED_RIGHT, 0);          
          delay(5000);
        break;
        
        case CROSSROAD_3:
          // Стоп
          analogWrite(SPEED_LEFT, 0);
          analogWrite(SPEED_RIGHT, 0);
          delay(100);

          // Поворот на 90
          digitalWrite(DIR_LEFT, LOW);
          analogWrite(SPEED_LEFT, SPEED);
          analogWrite(SPEED_RIGHT, SPEED + 5);
          delay(700);

          // Стоп
          analogWrite(SPEED_LEFT, 0);
          analogWrite(SPEED_RIGHT, 0);
          delay(100);

          // Немного назад
          digitalWrite(DIR_RIGHT, LOW);
          analogWrite(SPEED_LEFT, SPEED);
          analogWrite(SPEED_RIGHT, SPEED + 5);
          delay(200);

          // Стоп
          analogWrite(SPEED_LEFT, 0);
          analogWrite(SPEED_RIGHT, 0);
          delay(100);
          
          digitalWrite(DIR_LEFT, HIGH);
          digitalWrite(SPEED_RIGHT, HIGH);
        break;

        case END:
          analogWrite(SPEED_LEFT, 0);
          analogWrite(SPEED_RIGHT, 0);

          // Приехали на базу
          while(1);
        break;
      }

      lable_millis = millis();
    }
  }
  else {
    if ((millis() - lable_millis) > 700) {
      // Считаем, что мы не на метке только спустя 1 секунду после того, как наехали на неё
      on_lable = false;
    }
  }
 
    // В какое состояние нужно перейти?
    int targetState;
 
    if (left == right) {
        // под сенсорами всё белое или всё чёрное
        // едем вперёд
        targetState = STATE_FORWARD;
    } else if (left) {
        // левый сенсор упёрся в трек
        // поворачиваем налево
        targetState = STATE_LEFT;
    } else {
        targetState = STATE_RIGHT;
    }
 
    if (state == STATE_FORWARD && targetState != STATE_FORWARD) {
        int brakeTime = (currentSpeed > SLOW_SPEED) ?
            currentSpeed : 0;
        stepBack(brakeTime, targetState);
     }
 
    switch (targetState) {
        case STATE_FORWARD:
            runForward();
            break;
 
        case STATE_RIGHT:
            steerRight();
            break;
 
        case STATE_LEFT:
            steerLeft();
            break;
    }
 
}
