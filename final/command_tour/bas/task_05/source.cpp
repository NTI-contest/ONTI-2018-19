//============================================================================
// Подкоючение библиотек

//----------------------------------------------------------------------------
// Стандартные
#include <SPI.h>
#include <SD.h>
#include <Servo.h>
#include <math.h>

//----------------------------------------------------------------------------
// Пользовательские
#include "common.h"
#include "TinyGPSpp.h"

//============================================================================
// Определения

// Если определено, то система ждет сигнала с ГНСС, проверяет его валидность и
// рассчитывает стартовую точку. Для тестов в помещении можно закомментировать
#define GNSS_ENABLED

//============================================================================
// Периферийные устройства

//----------------------------------------------------------------------------
// ГНСС (NMEA)

// основной класс (строка $GPGGA)
TinyGPSPlus gps;

// дополнительные классы
// индикатор захвата позиции
TinyGPSCustom TGPSC_positionFixIndicator(gps, "GPGGA", 6);

// поправка по высоте [м]
TinyGPSCustom TGPSC_geoidSeparation(gps, "GPGGA", 11);

// угол пути [градусы]
TinyGPSCustom TGPSC_heading_deg(gps, "GPVTG", 1);

// горизонтальная скорость [км/ч]
TinyGPSCustom TGPSC_horizontalVelocity_kh(gps, "GPVTG", 7);

// скорость последовательного порта
const uint32_t GPS_BAUD_RATE = 38400;

// Измерения
const int N_GNSS = 1;    // число замеров для фильтрации
const int N_GNSS_0 = 20;  // число точек для вычисления начальной позиции

// время последнего вызова чтения датчиков [мс]
unsigned long int TLC_MS_GNSS = 0;
// мгновенные замеры
uint8_t hours, minutes, seconds;  // часы, минуты, секунды
int nSats;              // число спутников
double hdop;            // горизонтальный геометрический фактор
int pfi;              // индикатор захвата позиции

// массивы замеров
double latitudes[N_GNSS];         // широта [градусы]
double longitudes[N_GNSS];        // долгота [градусы]
double altitudesMsl[N_GNSS];      // высота над уровнем моря [м]
double headings[N_GNSS];        // угол пути [рад]
double horizontalVelocities[N_GNSS];  // модуль горизонтальной скорости [м/с]

// осредненные оценки
double initialLatitude = 0.0;   // широта точки старта [градусы]
double initialLongitude = 0.0;    // долгота точки старта [градусы]
double latitude = 0.0;        // широта [градусы]
double longitude = 0.0;       // долгота [градусы]
double altitudeMsl = 0.0;     // высота над уровнем моря [м]
double heading = 0.0;       // угол пути [рад]
double horizontalVelocity = 0.0;  // модуль горизонтальной скорости [м/с]

// рассчитываеме параметры
double velocityNorth = 0.0; // северная проекция скорости [м/с]
double velocityEast = 0.0;  // восточная проекция скорости [м/с]

const int N_SATS_MIN = 7;  // минимальное число спутников

// функция настройки
extern void setupMt3333();

// функция чтения
extern void readMt3333();

//---------------------------------------------------------------------------
// SD карта
File sdLog;                 // файл записи данных
String sdLogData;               // строка данных
unsigned long int T_MS_AUTOSAVE = 30000;  // период автосохранения
unsigned long int TLC_MS_AUTOSAVE = 0;    // время последнего автосохранения
unsigned long int T_MS_SD = 50;       // период записи
unsigned long int TLC_MS_SD = 0;        // время последней записи

extern void sdWrite();  // функция записи

//===========================================================================
// Система управления
int pwmAil = 1500;    // значение ШИМ управления
Servo AIL;        // ШИМ канал элероны расположены на ножке 2
int D_PWM_MAX = 300;  // максимальное изменение ШИМ относительно 1500
double eps = 0.0;   // сигнал рассогласования

// флаг режима полета ручка\автопилот
bool mode = false;
const int MODE_PIN = 35;


//=========================================================================
/***************************** ПОЛЕТ ПО КУРСУ ****************************/
float presetCoordinates[2] = {56.097714, 35.878395};	// координаты метки
#define SETPOINT_RADIUS 5	// Окрестность точки, в которой провести съемку
#define HEADING_P       4	// Коэффициент П регулятора
/*************************************************************************/


//=========================================================================
// Функция основной программы: инициализация
void setup()
{
  // на всякий случай :Р
  delay(5000);
  Serial2.print("START\n");

  //---------------------------------------------------------------------
  // Инициализация последовательного порта
  Serial.begin(115200); while (!Serial) {
    ;  // порт отладки
  }
  Serial2.begin(19200); while (!Serial2) {
    ;  // порт телеметрии
  }
  delay(5000);
  //---------------------------------------------------------------------
  // Инициализация ГНСС
  setupMt3333();
  //---------------------------------------------------------------------
  // Инициализация SD карты
  if (SD.begin(SD_CHIP_SELECT_PIN)) Serial2.print("SD RDY\n");
  else Serial2.print("SD NOT FOUND\n");
  sdLog = SD.open("log.txt", FILE_WRITE);

  //---------------------------------------------------------------------
  // подключение каналов управления
  AIL.attach(2);  // Прикрепляем ногу
  AIL.write(1500); // Задаем скорость.



  pinMode(MODE_PIN, INPUT);
  pinMode(4, OUTPUT);//ПИН КАМЕРЫ
}

//===========================================================================
// Функция основной программы: цикл
void loop()
{
	//-------------------------------------------------------------------------
	// Получение данных с ГНСС приемника
	readMt3333(); // Тут вы получаете heading, latitude, longitude с GPS

	/***********************************************************************/
	/**                          Начало разработки                        **/
	/***********************************************************************/
	// Курс на метку
	double courseToPreset = TinyGPSPlus::courseTo(latitude, longitude, 
				presetCoordinates[0], presetCoordinates[1]);

	// Расстояние до метки
	unsigned long distanceToPreset = 
		(unsigned long) TinyGPSPlus::distanceBetween(latitude, longitude, 
		presetCoordinates[0], presetCoordinates[1]);
		
	//Включение камеры в заданном радиусе до точки
	if(distanceToPreset <= SETPOINT_RADIUS) digitalWrite(4, 1);
	else digitalWrite(4, 0);

	// Стабилизатор курса
	double set_roll = constrain(1500 + 
		HEADING_P*(courseToPreset - heading), 1350, 1650);

	// Расчет управления на стабилизатор крена
	double Koeff = 2.0;		// коэффициент перевода градусов в ШИМ
	pwmAil = constrain(1500 + 
		Koeff*(map(set_roll, 1000, 2000, -20, 20)), 1350, 1650);

	// Выдача ШИМ
	AIL.writeMicroseconds(pwmAil);
	/***********************************************************************/
	/**                           Конец разработки                        **/
	/***********************************************************************/
	
	if (digitalRead(MODE_PIN) != mode)
	{
		mode = digitalRead(MODE_PIN);
		Serial.print("mode = " + String(mode) + "\n");
	}

	// сохранение на SD карту
	if (millis() - TLC_MS_SD > T_MS_SD)
	{
		TLC_MS_SD = millis();
		sdWrite();
	}
}

//============================================================================
// Функция настройки MT3333
void setupMt3333()
{
  //--------------------------------------------------------------------------
  // открытие последовательного порта
  Serial1.begin(GPS_BAUD_RATE); while (!Serial1) {
    ;
  }

#ifdef GNSS_ENABLED
  //--------------------------------------------------------------------
  // рассчет начального положения

  // 1. ожидание спутников
  Serial2.println("Searching sattelites");
  unsigned long int gnssTimer = millis();
  while ((nSats < N_SATS_MIN) && (millis() - gnssTimer < 60000))
  {
    delay(500);
    while (Serial1.available() > 0)
    {
      if (gps.encode(Serial1.read()))
      {
        nSats = gps.satellites.value();
        Serial2.print("nSats = ");
        Serial2.println(nSats);
      }
    }
  }

  // 2. расчет среднего начального положения
  int i = 0;
  while (i < N_GNSS_0)
  {
    while (Serial1.available())
    {
      if (gps.encode(Serial1.read()))
      {
        initialLatitude += gps.location.lat();
        initialLongitude += gps.location.lng();
        Serial2.print(gps.location.lat()); Serial2.print("\t");
        Serial2.print(gps.location.lng()); Serial2.print("\n");
        i++;
      }
    }
  }
  initialLatitude /= float(N_GNSS_0);
  initialLongitude /= float(N_GNSS_0);

  Serial2.print("Number of satellites found: ");
  Serial2.print(nSats); Serial2.print("\n");
  Serial2.print("Initial Latitude:  ");
  Serial2.print(initialLatitude, 8); Serial2.print("\n");
  Serial2.print("Initial Longitude: ");
  Serial2.print(initialLongitude, 8); Serial2.print("\n");
#endif //GNSS_ENABLED
}

//============================================================================
// Функция чтения MT3333
void readMt3333()
{
  //------------------------------------------------------------------------
  // Получение данных с ГНСС приемника
  while (Serial1.available() > 0)
  {
    if (gps.encode(Serial1.read()))
    {
      // мгновенные замеры
      hours = gps.time.hour();
      minutes = gps.time.minute();
      seconds = gps.time.second();
      nSats = gps.satellites.value();
      hdop = gps.hdop.value();
      pfi = atoi(TGPSC_positionFixIndicator.value());

      // фильтруемые замеры
      // 1. Заполнение массивов
      shiftArray(latitudes, N_GNSS, gps.location.lat());
      shiftArray(longitudes, N_GNSS, gps.location.lng());
      shiftArray(altitudesMsl, N_GNSS, gps.altitude.meters() + 
                  atof(TGPSC_geoidSeparation.value()));
      shiftArray(headings, N_GNSS, 
                  atof(TGPSC_heading_deg.value()) * DEG2RAD); //для mt3333
      shiftArray(horizontalVelocities, N_GNSS, 
                  atof(TGPSC_horizontalVelocity_kh.value()) * KH2MS);

      //Serial2.println(gps.course.deg());

      // 2. фильтрация скользящим средним
      latitude = mean(latitudes, N_GNSS);
      longitude = mean(longitudes, N_GNSS);
      altitudeMsl = mean(altitudesMsl, N_GNSS);
      heading = mean(headings, N_GNSS);
      horizontalVelocity = mean(horizontalVelocities, N_GNSS);

      // рассчитываеме параметры
      velocityNorth = horizontalVelocity * cos(heading);
      velocityEast = horizontalVelocity * sin(heading);
    }
  }
}

//============================================================================
// функция записи результатов измерений на SD карту
void sdWrite()
{
  //--------------------------------------------------------------------------
  // формирование строки сообщения

  sdLogData = String(millis()) + "\t" +
              String(latitude, 10) + "\t" +
              String(longitude, 10) + "\t" +
              String(heading * RAD2DEG) + "\t" +
              String(mode) + "\t" +
              String(pwmAil) + "\n";

  //--------------------------------------------------------------------------
  // запись сообщения
  if (sdLog) sdLog.println(sdLogData);

  //--------------------------------------------------------------------------
  // автосохранение данных
  if (millis() - TLC_MS_AUTOSAVE > T_MS_AUTOSAVE)
  {
    sdLog.close();
    SD.begin(SD_CHIP_SELECT_PIN);
    sdLog = SD.open("log.txt", FILE_WRITE);
    TLC_MS_AUTOSAVE = millis();
  }
}
