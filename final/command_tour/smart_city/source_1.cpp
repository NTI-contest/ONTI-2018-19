
// --------------------------------------------------------

#define LED_PIN                 23
#define PUMP_PIN                21
#define LED_STRIP_PIN           22

#define GATE_SERVO_PIN          3
#define GATE_LS_INSIDE_PIN      A2
#define GATE_LS_OUTSIDE_PIN     A1
#define GATE_LS_THRESHOLD       2.0f

#define BUZZER_PIN              2

#define CURRENT_SENSOR_PIN      A0

#define DISPLAY_CS_PIN          29
#define DISPLAY_SCK_PIN         28
#define DISPLAY_MOSI_PIN        27

#define HUMIDITY_PIN            4

#define FLOW_SENSOR_PIN         20 // 2, 3, 18, 19, 20, 21

#define RGB_PIN                 5
#define RGB_NUM                 3

#define BLE_SERIAL              Serial1
//#define BLE_TX_PIN              18  // Serial1
//#define BLE_RX_PIN              19  // Serial1

#define LORA_SERIAL             Serial2
//#define LORA_TX_PIN             17  // Serial2
//#define LORA_RX_PIN             16  // Serial2
#define LORA_RESET_PIN          15

//#define RADIO_MOSI_PIN          51
//#define RADIO_MISO_PIN          50
//#define RADIO_SCK_PIN           52
#define RADIO_CSN_PIN           47
#define RADIO_CE_PIN            46

// --------------------------------------------------------

class Dout {
  public:
  
  Dout(int pin):pin(pin) {
    pinMode(pin, OUTPUT);
  }

  void on() {
    digitalWrite(pin, 1);
  }

  void off() {
    digitalWrite(pin, 0);
  }

  private:

  int pin;
};

// --------------------------------------------------------
// --------------------------------------------------------

// --------------------------------------------------------
// Светодиод Пиранья
// --------------------------------------------------------

Dout led(LED_PIN);

// --------------------------------------------------------
// Помпа (Силовой ключ)
// --------------------------------------------------------

Dout pump(PUMP_PIN);

// --------------------------------------------------------
// Светодиодная лента (Силовой ключ)
// --------------------------------------------------------

Dout led_strip(LED_STRIP_PIN);

// --------------------------------------------------------
// RGB лента
// --------------------------------------------------------

#include <FastLED.h>

CRGB leds[RGB_NUM];

// --------------------------------------------------------
// Шлагбаум
// --------------------------------------------------------

#include <Servo.h>
#include <TroykaLight.h>

class Gate {
  public:
  
  Gate(uint8_t servo_pin, uint8_t ls_inside_pin, uint8_t ls_outside_pin):
        servo_pin(servo_pin),ls_inside(ls_inside_pin),ls_outside(ls_outside_pin) {
  }

  void begin() {
    servo.attach(servo_pin);
  }
  
  void open() {
    servo.write(0);
  }

  void close() {
    servo.write(90);
  }

  bool is_car_near_inside() {
    ls_inside.read();
//    Serial.print("ls_inside: ");
//    Serial.println(ls_inside.getLightLux());
    return ls_inside.getLightLux() < GATE_LS_THRESHOLD;
  }

  bool is_car_near_outside() {
    ls_outside.read();
//    Serial.print("ls_outside: ");
//    Serial.println(ls_outside.getLightLux());
    return ls_outside.getLightLux() < GATE_LS_THRESHOLD;
  }

  private:
  
  TroykaLight ls_inside;
  TroykaLight ls_outside;
  uint8_t servo_pin;
  Servo servo;
};

Gate gate(GATE_SERVO_PIN, GATE_LS_INSIDE_PIN, GATE_LS_OUTSIDE_PIN);

// --------------------------------------------------------
// Базер
// --------------------------------------------------------

class Buzzer {
  public:

  Buzzer(uint8_t pin):pin(pin) {
  }

  void on() {
    tone(pin, 4000);
  }
  
  void on(int duration) {
    tone(pin, 4000, duration);
  }

  void off() {
    noTone(pin);
  }

  private:

  uint8_t pin;
};

Buzzer buzz(BUZZER_PIN);

// --------------------------------------------------------
// Датчик тока
// --------------------------------------------------------

#include <TroykaCurrent.h>

ACS712 sensorCurrent(CURRENT_SENSOR_PIN);

float read_current() {
  return sensorCurrent.readCurrentDC();
}

// --------------------------------------------------------
// 7-сегментный индикатор
// --------------------------------------------------------

#include <QuadDisplay2.h>

QuadDisplay display(DISPLAY_CS_PIN, DISPLAY_MOSI_PIN, DISPLAY_SCK_PIN);

// --------------------------------------------------------
// Датчик влажности и температуры
// --------------------------------------------------------

#include <TroykaDHT.h>

DHT dht(HUMIDITY_PIN, DHT11);

// --------------------------------------------------------
// Датчик потока воды
// --------------------------------------------------------

class FlowSensor {
  public:
  
  FlowSensor(uint8_t pin):pin(pin) {
  }

  void begin() {
    attachInterrupt(digitalPinToInterrupt(pin), irq_callback, RISING);
    reset();
  }

  void reset() {
    tick_volume = 0;
    start_time = millis();
  }

  float get_volume() {
    return (float)tick_volume / 450;
  }
  
  private:

  uint8_t pin;
  unsigned long start_time;
  static volatile unsigned int tick_volume;

  static void irq_callback() {
    tick_volume++;
  }
};

volatile unsigned int FlowSensor::tick_volume = 0;

FlowSensor flow_sensor(FLOW_SENSOR_PIN);

// --------------------------------------------------------
// BLE
// --------------------------------------------------------

class BLE {
  public:
  
  void begin() {
    BLE_SERIAL.setTimeout(200);
    
    at("AT");
    Serial.print("BLE: AT -> ");
    String str = BLE_SERIAL.readString();
    Serial.println(str);
  
    at("AT+ROLE1");
    Serial.print("BLE: AT+ROLE1 -> ");
    str = BLE_SERIAL.readString();
    Serial.println(str);
  
    at("AT+IMME1");
    Serial.print("BLE: AT+IMME1 -> ");
    str = BLE_SERIAL.readString();
    Serial.println(str);
    Serial.println();
  }

  void at(const char *str) {
    BLE_SERIAL.print(str);
  }

  private:
};

BLE ble;

// --------------------------------------------------------
// LoRa
// --------------------------------------------------------

class Lora {
  public:

  Lora(int pin):reset_pin(pin) {
    pinMode(reset_pin, OUTPUT);
  }

  bool begin(void)
  {
    digitalWrite(reset_pin, 0);
    delay(200);
    digitalWrite(reset_pin, 1);

    LORA_SERIAL.setTimeout(200);
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());
//    delay(200);
    
    LORA_SERIAL.println("at+version");
    Serial.print("LoRa: at+version -> ");
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());

//    LORA_SERIAL.println("at+uart=9600,8,0,0,0");
//    Serial.print("LoRa: at+uart -> ");
//    while (!LORA_SERIAL.available());
//    Serial.println(LORA_SERIAL.readString());

//    LORA_SERIAL.begin(9600);

    LORA_SERIAL.println("at+mode=0");
    Serial.print("LoRa: at+mode=0 -> ");
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());

    LORA_SERIAL.println("at+set_config=dev_eui:0000111122223333");
    Serial.print("LoRa: at+set_config=dev_eui.. -> ");
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());

    LORA_SERIAL.println("at+set_config=app_eui:70B3D57ED00149AF&app_key:BC93A26C264C35404909D723DDBF977D");
    Serial.print("LoRa: at+set_config=app_eui.. -> ");
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());

    LORA_SERIAL.println("at+join=otaa");
    Serial.print("LoRa: at+join=otaa -> ");
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());  // OK
    while (!LORA_SERIAL.available());
    Serial.println(LORA_SERIAL.readString());  // at+recv=3,0,0

//    LORA_SERIAL.setTimeout(1000);
  }

  String send(String str) {
    String ans;

    if (!_transmitting) {
      String hex_str = str2hex(str);
  
      Serial.println(str + " (" + hex_str + ")");

      LORA_SERIAL.println("at+send=0,2," + hex_str);
      ans = LORA_SERIAL.readStringUntil('\n');
      Serial.println(ans);  // OK

      _transmitting = true;
      _busy = true;
    }
    
    if (LORA_SERIAL.available()) {
      ans = LORA_SERIAL.readStringUntil('\n');  // at+recv
      Serial.println(ans);
      
      // Подтверждение
      if (ans.startsWith("at+recv=2,0,0")) {
        _transmitting = false;
        _busy = false;

        // at+recv=0,2
        ans = LORA_SERIAL.readStringUntil('\n');  // at+recv
//        Serial.println(ans);
      }

      // Входящие данные
      if (ans.startsWith("at+recv=0,2")) {
        Serial.println(ans);
        ans.remove(0, ans.indexOf(",") + 1);
        ans.remove(0, ans.indexOf(",") + 1);
        ans.remove(0, ans.indexOf(",") + 1);
        ans.remove(0, ans.indexOf(",") + 1);
        ans.remove(0, ans.indexOf(",") + 1);
        ans.trim();
        String ret = hex2str(ans);
        Serial.println(ret + " (" + ans + ")");
        
        return ret;
      }
    }
    
    return "";
  }

  bool busy() {
    return _busy;
  }

  private:

  int reset_pin;
  const char* const lut = "0123456789ABCDEF";
  bool _transmitting = false;
  bool _busy = false;

  String str2hex(String str) {
    size_t len = str.length();
    
    String hex_str;
    hex_str.reserve(2 * len);
    
    for (size_t i = 0; i < len; ++i) {
      const unsigned char c = str[i];
      hex_str += lut[c >> 4];
      hex_str += lut[c & 15];
    }

    return hex_str;
  }

  String hex2str(String hex_str) {
    size_t hex_len = hex_str.length();
    if (hex_len & 1 || hex_len == 0) {
      return "";
    }
    
    size_t len = hex_len / 2;
    
    String str;
    str.reserve(len);
    
    for (size_t i = 0, j = 0; i < len; i++, j++) {
      char res;
      res = (hex_str[j] & '@' ? hex_str[j] + 9 : hex_str[j]) << 4, j++;
      res |= (hex_str[j] & '@' ? hex_str[j] + 9 : hex_str[j]) & 0xF;

      str += res;
    }
    
    return str;
  }
};

Lora lora(LORA_RESET_PIN);

// --------------------------------------------------------
// --------------------------------------------------------

// ========================================================
// Application
// ========================================================

 uint32_t traffic_lights_poll() {
  static const unsigned long period = 1000;
  static uint32_t current_color = CRGB::Red;
  static uint32_t pre_color = CRGB::Yellow;
  static unsigned long last_millis = 0;
  static byte cnt = 0;

  if (millis() - last_millis > period) {
    switch(current_color) {
      case CRGB::Red:
        if (++cnt < 5) {
          break;
        }
        cnt = 0;
      
        current_color = CRGB::Yellow;
        pre_color = CRGB::Red;
        
        leds[2] = CRGB::Red;
        leds[1] = CRGB::Yellow;
        leds[0] = CRGB::Black;
      break;

      case CRGB::Yellow:
        if (pre_color == CRGB::Red) {
          current_color = CRGB::Green;

          leds[2] = CRGB::Black;
          leds[1] = CRGB::Black;
          leds[0] = CRGB::Green;
        }
        else if (pre_color == CRGB::Green) {
          current_color = CRGB::Red;

          leds[2] = CRGB::Red;
          leds[1] = CRGB::Black;
          leds[0] = CRGB::Black;
        }
        
        pre_color = CRGB::Yellow;
      break;

      case CRGB::Green:
        if (++cnt < 5) {
          break;
        }
        cnt = 0;
        
        current_color = CRGB::Yellow;
        pre_color = CRGB::Green;

        leds[2] = CRGB::Black;
        leds[1] = CRGB::Yellow;
        leds[0] = CRGB::Black;
      break;
    }

    last_millis = millis();
    FastLED.show();
  }

  return current_color;
}

void gate_poll() {
  typedef enum {
    IN_PARK,
    NEAR_INSIDE,
    UNDER_GATE,
    NEAR_OUTSIDE,
    IN_CITY
  } gate_state_t;

  typedef enum {
    EXIT,
    ENTER
  } gate_type_t;

  static gate_state_t gate_state = IN_PARK;
  static gate_type_t gate_type = EXIT;

  switch (gate_state) {
    case IN_PARK:
      if (gate.is_car_near_inside()) {
        gate.open();
        gate_state = NEAR_INSIDE;
      }
      break;
      
    case NEAR_INSIDE:
      if (!gate.is_car_near_inside()) {
        if (gate_type == EXIT) {
          gate_state = UNDER_GATE;
        }
        else {
          gate.close();
          gate_state = IN_PARK;
          gate_type = EXIT;
        }
      }
      break;
      
    case UNDER_GATE:
      if (gate_type == EXIT) {
        if (gate.is_car_near_outside()) {
          gate_state = NEAR_OUTSIDE;
        }
      }
      else {
        if (gate.is_car_near_inside()) {
          gate_state = NEAR_INSIDE;
        }
      }
      break;
      
    case NEAR_OUTSIDE:
      if (!gate.is_car_near_outside()) {
        if (gate_type == EXIT) {
          gate.close();
          gate_state = IN_CITY;
          gate_type = ENTER;
        }
        else {
          gate_state = UNDER_GATE;
        }
      }
      break;
      
    case IN_CITY:
      if (gate.is_car_near_outside()) {
        gate.open();
        gate_state = NEAR_OUTSIDE;
      }
      break;
      
    default:
      break;
  }
}

#define BEACON    "CE98F7E99E96"

bool ble_poll() {
//  static bool disc_started = false;
  static String dis_rsp = "";
  static const int8_t cnt_initial = 80;
  static int8_t cnt = cnt_initial;
  static bool ret = false;

  if (cnt == cnt_initial) {
    cnt--;
    Serial1.setTimeout(50);
    Serial1.print("AT+DISI?");
//    Serial.print("BLE: DISI? -> ");
  }
  else {
    cnt--;
    String str = Serial1.readString();
    dis_rsp.concat(str);
    
    if (str.endsWith("DISCE")) {
//      Serial.println(dis_rsp);
      ret = false;
      
      if (dis_rsp.indexOf(":"BEACON":") > 0) {
        Serial.println("iBeacon found");

        ret = true;
      }

      dis_rsp = "";
      cnt = cnt_initial;
    }
  }

  if (!ret) {
    static unsigned long last_millis = 0;
    static bool on = false;
    unsigned long current_millis = millis();
    
    if (current_millis - last_millis > 1000) {
      last_millis = current_millis;

      if (on) {
        on = false;
        led.off();
        buzz.off();
      }
      else {
        on = true;
        led.on();
        buzz.on();
      }
    }
  }
  else {
    led.off();
    buzz.off();
  }
  
  return ret;
}

float current = 0;
float humidity = 0;
float temperature = 0;
float flow = 0;
int car_lable = 0;
bool beacon = false;
bool taxi = false;

String lora_send_data() {
  static byte part = 0;
  String str = String("");

  if (!lora.busy()) {
    part++;

    str.concat((String)"{");
    
    switch (part) {
      case 1:
        str.concat((String)"\"h\":\""  + humidity    + "\",");
        str.concat((String)"\"t\":\""  + temperature + "\"");
      break;
  
      case 2:
        str.concat((String)"\"c\":\""  + current     + "\",");
        str.concat((String)"\"f\":\""  + flow        + "\"");
      break;
  
      case 3:
        str.concat((String)"\"cr\":\"" + car_lable   + "\",");
        str.concat((String)"\"b\":\""  + beacon      + "\"");
      break;
    }

    str.concat((String)"}");

    if (part >= 3) {
      part = 0;
    }
  }

  String ans_hex = lora.send(str);

  return ans_hex;
}

void setup() {
  Serial.begin(115200);
  Serial.println("\nStart program!\n");

  gate.begin();
  gate.close();

  display.begin();
  display.displaySegments((uint32_t)QD_MINUS | (uint32_t)QD_MINUS << 8 | (uint32_t)QD_MINUS << 16 | (uint32_t)QD_MINUS << 24);

  dht.begin();

  flow_sensor.begin();

  led_strip.on();
  
  FastLED.addLeds<WS2811, RGB_PIN, GRB>(leds, RGB_NUM);
  FastLED.clear(true);
  leds[2] = CRGB::Red;
  leds[1] = CRGB::Black;
  leds[0] = CRGB::Black;
  FastLED.show();

  BLE_SERIAL.begin(9600);
  ble.begin();

  LORA_SERIAL.begin(9600);
  lora.begin();
  
  led.on();
  buzz.on();
  delay(100);
  led.off();
  buzz.off();

  radio_begin();
}

void loop() {
  display.displayFloat(flow, 2, true);

  dht.read();

  current = abs(read_current());
  humidity = dht.getHumidity();
  temperature = dht.getTemperatureC();
  flow = flow_sensor.get_volume();

//  Serial.println((String)"Current: " + current + " A");
//  Serial.println((String)"Humidity: " + humidity + " %");
//  Serial.println((String)"Temperature: " + temperature + " C");
//  Serial.println((String)"Flow: " + flow + " l");

  gate_poll();

  uint32_t color = traffic_lights_poll();

  char radio_buff[64];
  sprintf(radio_buff, "color:%s", color == CRGB::Green ? "green" : "red");
  if (taxi) {
    strcat(radio_buff, ",taxi");
  }
  
  radio_write(radio_buff, strlen(radio_buff));
  int len = radio_read(radio_buff, 10);
  int sret = sscanf(radio_buff, "station: %d", &car_lable);
  if (sret == 1 && car_lable > 0) {
    Serial.print("New car station: ");
    Serial.println(car_lable);
  }

  beacon = ble_poll();

  String cmd = lora_send_data();
//   {"method":"light","params":true}
  if (cmd.substring(11, 16) == "light") {    
    if (cmd.endsWith("true}")) {
      led_strip.on();
    }
    else if (cmd.endsWith("false}")) {
      led_strip.off();
    }
    else {
      Serial.println("Error");
    }
  }
  else if (cmd.substring(11, 16) == "water") {
    if (cmd.endsWith("true}")) {
      pump.on();
    }
    else if (cmd.endsWith("false}")) {
      pump.off();
    }
    else {
      Serial.println("Error");
    }
  }
  else if (cmd.substring(11, 15) == "taxi") {
    if (cmd.endsWith("true}")) {
      taxi = true;
    }
    else if (cmd.endsWith("false}")) {
      taxi = false;
    }
    else {
      Serial.println("Error");
    }
  }

//  delay(500);
}
