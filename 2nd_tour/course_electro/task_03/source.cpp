#define INPUT 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define HIGH 1
#define LOW 0

void delay(int ms);
void digitalWrite(int pin, int value);
void pinMode(int pin, int mode);
int LED_PIN;   // каким пином мигаем
int ON_PERIOD; // время свечения, мс
int OFF_PERIOD; // интервал между миганиями, мс
void setup()
{
  pinMode(LED_PIN, OUTPUT); 
}

void loop()
{
  // и тут как-то все не так..  
  digitalWrite(LED_PIN, HIGH); 
  delay(ON_PERIOD);                     
  digitalWrite(LED_PIN, LOW);  
  delay(OFF_PERIOD);                     
}

#include <iostream>
long __timer = 0;
bool __pins[13], __pins_out[13];
void delay(int ms)
{
    __timer += ms;
}

void pinMode(int pin, int mode)
{
     if( pin >= 0 && pin <= 13 ){
        __pins_out[pin] = (mode == OUTPUT);
        __pins[pin] = (mode == INPUT_PULLUP);
     }
}
void digitalWrite(int pin, int value)
{
    value = !!value;  // normalize to 0 or 1
    if( pin >= 0 && pin <= 13 && __pins[pin] != value ){
        __pins[pin] = value;
        if( __pins_out[pin] )
            printf("%06dDW%02d=%d\n", __timer, pin, value);
    }
}
int main()
{
    __timer = 0;
    std::cin >> LED_PIN >> ON_PERIOD >> OFF_PERIOD;
    setup();
    for(int i = 0;  i < 3; i++)
    {
        loop();
    }
    return 0;
}
