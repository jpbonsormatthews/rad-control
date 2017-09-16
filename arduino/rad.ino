#include <OneWire.h>
#include <DallasTemperature.h>
#include <stdint.h>

// on board LED
int led = 13;

// Shift out defines
int latchPin = 5;
int clockPin = 6;
int dataPin = 4;
int resetPin = 7;

// Temp defines
enum Zones {
  LivingRoom_FrontBack = 0,
  Kitchen_Toilet = 1,
  Hall = 2,
  SofiaBed = 3,
  Front_Back_Bed = 4,
  Study = 5,
  Bathroom = 6,
  NUM_ZONES = Bathroom + 1,
};
unsigned char TempBuses[NUM_ZONES] = {
  12, // LivingRoom_FrontBack
  11, // Kitchen_Toilet
  10, // Hall
  9, // SofiaBed
  2, // Front_Back_Bed
  3, // Study
  8, // Bathroom
};
OneWire oneWires[NUM_ZONES] = {
  OneWire(TempBuses[LivingRoom_FrontBack]),
  OneWire(TempBuses[Kitchen_Toilet]),
  OneWire(TempBuses[Hall]),
  OneWire(TempBuses[SofiaBed]),
  OneWire(TempBuses[Front_Back_Bed]),
  OneWire(TempBuses[Study]),
  OneWire(TempBuses[Bathroom]),
};
DallasTemperature sensors[NUM_ZONES] = {
  DallasTemperature(&oneWires[LivingRoom_FrontBack]),
  DallasTemperature(&oneWires[Kitchen_Toilet]),
  DallasTemperature(&oneWires[Hall]),
  DallasTemperature(&oneWires[SofiaBed]),
  DallasTemperature(&oneWires[Front_Back_Bed]),
  DallasTemperature(&oneWires[Study]),
  DallasTemperature(&oneWires[Bathroom]),
};

#define DALLAS_UID 0x33

void setup(void)
{
  pinMode(led, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(resetPin, OUTPUT);

  // reset shift registers
  digitalWrite(resetPin, LOW);
  digitalWrite(dataPin, LOW);
  digitalWrite(latchPin, LOW);
  digitalWrite(clockPin, LOW);
  delay(100);
  digitalWrite(resetPin, HIGH);
  digitalWrite(clockPin, HIGH);
  digitalWrite(latchPin, HIGH);

  // set all outputs to off
  digitalWrite(latchPin, LOW);
  for (int i=5; i>=0; i--) {
    shiftOut(dataPin, clockPin, MSBFIRST, 0);
  }
  digitalWrite(latchPin, HIGH);

  digitalWrite(led, HIGH);   // turn the LED on

  // start serial port
  Serial.begin(9600);

  // Start up the library
  for (unsigned int i=0; i<NUM_ZONES; i++) {
    sensors[i].begin();
  }
}


void loop(void)
{
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    Serial.print(":::");
    Serial.print(cmd);
    Serial.println(":::");
    if (cmd == 'T') {
      // read temps
      Serial.println(">T");
      for (unsigned int i=0; i<NUM_ZONES; i++) {
        Serial.print("Z");
        Serial.print(i);
        sensors[i].requestTemperatures(); // Send the command to get temperatures

        Serial.print(":");
        unsigned int count = sensors[i].getDeviceCount();
        Serial.println(count);

        for (unsigned int j=0; j<count; j++) {
          Serial.print("Z");
          Serial.print(i);
          Serial.print("D");
          Serial.print(j);
          Serial.print(":");
          uint8_t addr[8];
          if (sensors[i].getAddress(addr, j)) {
            for (int a=0; a<8; a++) {
              Serial.print(addr[a], HEX);
              if (a<7) {
                Serial.print(".");
              }
            }
          } else {
            Serial.print("?");
          }
          Serial.print(":");
          Serial.println(sensors[i].getTempCByIndex(j));

        }
      }
      Serial.println("<T");
    }

    if (cmd == 'S') {
      // set outputs
      Serial.println(">S");
      uint8_t data[6];
      Serial.readBytes((char*)data, 6);
      for (int i=0; i<6; i++) {
        Serial.print(data[i], HEX);
        if (i<5) {
          Serial.print(".");
        }
      }
      Serial.println("");
      uint8_t crc = OneWire::crc8(data, 5);
      if (crc != data[5]) {
        Serial.print("Invalid crc, calculated:");
        Serial.println(crc,HEX);
      } else {
        digitalWrite(latchPin, LOW);
        for (int i=5; i>=0; i--) {
          shiftOut(dataPin, clockPin, MSBFIRST, data[i]);
        }
        digitalWrite(latchPin, HIGH);
      }
      Serial.println("<S");
    }
  }

}
