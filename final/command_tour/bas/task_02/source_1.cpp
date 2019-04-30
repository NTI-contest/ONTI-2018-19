// Программа ручной калибровки датчика MPU9250
#include "MPU9250.h"
#include "common.h"

//============================================================================
// Переменные

// Датчик MPU9250, адрес 0x68, шина I2C
MPU9250 IMU(Wire,0x68);
int status;

//----------------------------------------------------------------------------
// измерения
float nx, ny, nz;	// кажущиеся ускорения [м/с2]
float wx, wy, wz;	// угловые скорости [рад/c]

// буфер замеров
const int N = 250;
float mes[N];

//----------------------------------------------------------------------------
// параметры калибровки

// гироскоп
float wx_b, wy_b, wz_b; // сдвиг нуля гироскопа

// акселерометр
float muxp, muxm;	// средние значения мин и макс измерений
float muyp, muym;
float muzp, muzm;
float kx, ky, kz;	// масштабный коэффициент акселерометра
float bx, by, bz;	// сдвиг нуля акселерометра

// буфер для чтения входной строки
uint8_t symbol;

// функции настройки и чтения
extern void setupImu();
extern void readImu();

//============================================================================
// Основная функция: настройка программы
void setup() {
  // открытие последовательного порта
  Serial.begin(115200); while(!Serial) { ; }
  
  // настройка датчика
  setupImu();
  
  // калибровка гироскопа: сдвиг нуля рассчитывается как среднее N замеров по каждой оси
  for (int k = 0; k < N; k++)
  {
    readImu();
    shiftArray(mes, N, wx);
    delay(20);
  }
  wx_b = mean(mes, N);

  for (int k = 0; k < N; k++)
  {
    readImu();
    shiftArray(mes, N, wy);
    delay(20);
  }
  wy_b = mean(mes, N);

  for (int k = 0; k < N; k++)
  {
    readImu();
    shiftArray(mes, N, wz);
    delay(20);
  }
  wz_b = mean(mes, N);
  
  // вывод сдвигов нуля гироскопа в порт
  Serial.print("gyro bias X = " + String(wx_b,6) + "\n");
  Serial.print("gyro bias Y = " + String(wy_b,6) + "\n");
  Serial.print("gyro bias Z = " + String(wz_b,6) + "\n");
  
}

//============================================================================
// основная функция: цикл
void loop() {
  // Калибровка акселерометра
  if (Serial.available() > 0)
  {
    // считать символ
    symbol = Serial.read();
    
    // очистить буфер
    while (Serial.available() > 0) Serial.read();
    
    // определить калибруемую ось
    // OX -------------------------------------------
    if (symbol == 'q')
    {
      for (int k = 0; k < N; k++)
      {
        readImu();
        shiftArray(mes, N, nx);
        delay(20);
      }
      muxp = mean(mes, N);
      Serial.print("muxp = " + String(muxp) + "\n");
    }
    
    if (symbol == 'w')
    {
      for (int k = 0; k < N; k++)
      {
        readImu();
        shiftArray(mes, N, nx);
        delay(20);
      }
      muxm = mean(mes, N);
      Serial.print("muxm = " + String(muxm) + "\n");
    }
    
    // OY -------------------------------------------
    if (symbol == 'e')
    {
      for (int k = 0; k < N; k++)
      {
        readImu();
        shiftArray(mes, N, ny);
        delay(20);
      }
      muyp = mean(mes, N);
      Serial.print("muyp = " + String(muyp) + "\n");
    }
    
   if (symbol == 'r')
    {
      for (int k = 0; k < N; k++)
      {
        readImu();
        shiftArray(mes, N, ny);
        delay(20);
      }
      muym = mean(mes, N);
      Serial.print("muym = " + String(muym) + "\n");
    }
    
    // OZ -------------------------------------------
    if (symbol == 't')
    {
      for (int k = 0; k < N; k++)
      {
        readImu();
        shiftArray(mes, N, nz);
        delay(20);
      }
      muzp = mean(mes, N);
      Serial.print("muzp = " + String(muzp) + "\n");
    }
    
    if (symbol == 'y')
    {
      for (int k = 0; k < N; k++)
      {
        readImu();
        shiftArray(mes, N, nz);
        delay(20);
      }
      muzm = mean(mes, N);
      Serial.print("muzm = " + String(muzm) + "\n");
    }
    
    // finish
    if (symbol == 'f')
    {
		// расчет калибровочных параметров акселерометра
      kx = 19.614/(muxp - muxm); bx = (muxp + muxm)/2.0;
      ky = 19.614/(muyp - muym); by = (muyp + muym)/2.0;
      kz = 19.614/(muzp - muzm); bz = (muzp + muzm)/2.0;

      Serial.print("acc bias X = " + String(bx,6) + "\t" 
        + "acc scale X = "+ String(kx,6) + "\n");
      Serial.print("acc bias Y = " + String(by,6) + "\t" 
        + "acc scale Y = "+ String(ky,6) + "\n");
      Serial.print("acc bias Z = " + String(bz,6) + "\t" 
        + "acc scale Z = "+ String(kz,6) + "\n");
      
      IMU.setAccelCalX(bx, kx);
      IMU.setAccelCalY(by, ky);
      IMU.setAccelCalZ(bz, kz);
      
      IMU.setGyroBiasX_rads(wx_b);
      IMU.setGyroBiasY_rads(wy_b);
      IMU.setGyroBiasZ_rads(wz_b);
      
	  // переход в нормальный режим работы
      while (1)
      {
        // read the sensor
        IMU.readSensor();

        // display the data
        Serial.print(IMU.getAccelX_mss(),6);  Serial.print("\t");
        Serial.print(IMU.getAccelY_mss(),6);  Serial.print("\t");
        Serial.print(IMU.getAccelZ_mss(),6);  Serial.print("\t");
        Serial.print(IMU.getGyroX_rads(),6);  Serial.print("\t");
        Serial.print(IMU.getGyroY_rads(),6);  Serial.print("\t");
        Serial.print(IMU.getGyroZ_rads(),6);  Serial.print("\n");
        delay(20);
      }
    }
    
  }

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
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
  
  // 50 Hz update rate
  IMU.setSrd(19);
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
