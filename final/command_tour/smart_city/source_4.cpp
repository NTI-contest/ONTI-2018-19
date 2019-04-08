
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "printf.h"

// --------------------------------------------------------

//#define RADIO_MOSI_PIN          11
//#define RADIO_MISO_PIN          12
//#define RADIO_SCK_PIN           13
#define RADIO_CSN_PIN           10
#define RADIO_CE_PIN            9

// --------------------------------------------------------

// Hardware configuration: Set up nRF24L01 radio on SPI bus plus pins 7 & 8 
RF24 radio(RADIO_CE_PIN, RADIO_CSN_PIN);

const byte addresses[][6] = {"00001", "00002"};

// --------------------------------------------------------

void radio_begin() {  
  radio.begin();
  printf_begin();
  radio.openWritingPipe(addresses[1]); // 00002
  radio.openReadingPipe(1, addresses[0]); // 00001
  radio.enableDynamicPayloads();
  radio.setPALevel(RF24_PA_MIN);

  radio.printDetails();     // Dump the configuration of the rf unit for debugging
}

bool radio_write(void *data, size_t len) {
  radio.stopListening();
  
  if (!radio.write(data, len)) {
    Serial.println(F("Radio tx failed"));
    return false;
  }

  return true;
}

int radio_read(void *data, int timeout) {
  uint8_t len = 0;
  radio.startListening();
  
  // Wait here until we get a response, or timeout
  unsigned long started_waiting_at = millis();
  bool _timeout = false;
  while ( !radio.available() && !_timeout ) {
    if (millis() - started_waiting_at > timeout)
    _timeout = true;
  }
  
  // Describe the results
  if (!_timeout) {
    // Grab the response, compare, and send to debugging spew
    len = radio.getDynamicPayloadSize();
    
    // If a corrupt dynamic payload is received, it will be flushed
    if(!len){
      return 0; 
    }
    
    radio.read(data, len);
    
    // Put a zero at the end for easy printing
    ((uint8_t*)data)[len] = 0;
    
    printf("Got data size = %d (%s)\r\n", len, (char*)data);
  }

  return len;
}
