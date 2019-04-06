// программа определения угла крена на основе комплексирования измерений 
// акселерометра и гироскопа с использованием фильтра Калмана
#include "MPU9250.h"

//============================================================================
// Переменные

// Датчик MPU9250, адрес 0x68, шина I2C
MPU9250 IMU(Wire,0x68);
int status;

// кажущиеся ускорения [м/с2]
float nx, ny, nz;

// угловые скорости [рад/c]
float wx, wy, wz;

// параметры калибровки (задаются вручную по результатам предыдущей программы)
float gyroBiasX = 0.000174;
float gyroBiasY = 0.000219;
float gyroBiasZ = 0.000143;

float accelBiasX = 0.113216;
float accelBiasY = 0.180062;
float accelBiasZ = -0.599224;

float accelScaleFactorX = 1.000751;
float accelScaleFactorY = 0.998263;
float accelScaleFactorZ = 0.991242;

// функции настройки и чтения
extern void setupImu();
extern void readImu();

// параметры оценивателя
float K = 0.1;		// коэффициент усиления
float xhatk = 0;	// оценка угла на текущем шаге
float xhatk_1 = 0;	// оценка угла на предыдущем шаге
float zk = 0.0;		// измерение угла по акселерометру
float wk = 0.0;		// угловая скорость на текущем шаге
float wk_1 = 0.0;	// угловая скорость на предыдущем шаге
unsigned long int t;	// время последнего вызова фильтра

//============================================================================
// Основная функция: настройка программы
void setup() 
{
  // открытие последовательного порта
  Serial.begin(115200); while(!Serial) { ; }
  
  // настройка датчика
  setupImu();
}

//============================================================================
// основная функция: цикл
void loop() 
{
	// чтение датчика
	readImu();
	
	// процедура определения угла крена
	wk = -wx;	// угловая скорость вокруг оси Ох связанной (!) системы координат
	zk = atan2(ny,-nz);	// угол крена по измерениям акселерометра
	// вычисление оценки: средневзвешенное между измерением и прогнозом
	xhatk = K*zk + (1.0 - K)*(xhatk_1 + wk_1*float(micros()-t)*1.0e-6);
	
	// сдвиг замеров
	t = micros();
	wk_1 = wk;
	xhatk_1 = xhatk;
	
	// вывод данных
	Serial.println(String(zk*57.3,6) +"\t"+ String(xhatk*57.3,6) +"\t"+ String(wk*57.3,6));
	
	// 50 Hz
	delay(20);
}

//============================================================================
// настройка датчика
void setupImu()
{
  status = IMU.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
  
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_2G);
  IMU.setGyroRange(MPU9250::GYRO_RANGE_250DPS);
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_184HZ);
  
  // 50 Hz update rate
  IMU.setSrd(19);
  
  IMU.setAccelCalX(accelBiasX, accelScaleFactorX);
  IMU.setAccelCalY(accelBiasY, accelScaleFactorY);
  IMU.setAccelCalZ(accelBiasZ, accelScaleFactorZ);
      
  IMU.setGyroBiasX_rads(gyroBiasX);
  IMU.setGyroBiasY_rads(gyroBiasY);
  IMU.setGyroBiasZ_rads(gyroBiasZ);
}

//============================================================================
// чтение датчика
void readImu()
{
  IMU.readSensor();
  
  nx = IMU.getAccelX_mss();
  ny = IMU.getAccelY_mss();
  nz = IMU.getAccelZ_mss();
  
  wx = IMU.getGyroX_rads();
  wy = IMU.getGyroY_rads();
  wz = IMU.getGyroZ_rads();
}
