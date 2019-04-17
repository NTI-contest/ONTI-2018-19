int LED_PIN;   // каким пином мигаем
int ON_PERIOD; // время свечения, мс
int OFF_PERIOD; // интервал между миганиями, мс
void setup()
{
    pinMode(LED_PIN,OUTPUT);
}
void loop()
{
    digitalWrite(LED_PIN, HIGH); 
    delay(ON_PERIOD);                     
    digitalWrite(LED_PIN, LOW);  
    delay(OFF_PERIOD);                     
}