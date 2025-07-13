#include <Servo.h>

Servo servo_1;

void setup() {
  Serial.begin(115200);
}

String byteToBinaryString(byte b) {
  String result = "";
  for (int i = 7; i >= 0; i--) {
    result += String((b >> i) & 1);
  }
  return result;
}

const int maxBytes = 16;
String byteArray[maxBytes];

void resetArray() {
  for (int i = 0; i < maxBytes; i++) {
    byteArray[i] = "00000000";
  }
}

int byteStringToDenary(String s)
{
  int coefficient = 128;
  int out = 0;
  for (int i = 0; i < 8; i++)
  {
    char bit = s[i];
    if (bit == '1')
    {
      out += coefficient;
    }
    coefficient /= 2;
  }
  return out;
}

uint8_t mode;

void loop() {
  if (Serial.available() > 0) {
    delay(5);

    resetArray();

    int index = 0;
    while (Serial.available() > 0 && index < maxBytes) {
      byte incoming = Serial.read();
      byteArray[index] = byteToBinaryString(incoming);
      index++;
    }

    if (byteArray[0].equals("00000001"))
    {
      Serial.println("Pin Mode Change");
      int pin = byteStringToDenary(byteArray[1]);
      if (byteArray[2].equals("00000010"))
      {
        mode = INPUT;
      }
      else
      {
        mode = OUTPUT;
      }

      pinMode(pin, mode);
    }
    else if (byteArray[0].equals("00000100"))
    {
      Serial.println("GPIO Digital Write");
      int pin = byteStringToDenary(byteArray[1]);
      if (byteArray[2].equals("00000101"))
      {
        mode = LOW;
      }
      else
      {
        mode = HIGH;
      }

      digitalWrite(pin, mode);
    }
    else if (byteArray[0].equals("00000111"))
    {
      Serial.println("Servo_1 Attach");
      int pin = byteStringToDenary(byteArray[1]);
      servo_1.attach(pin);
    }
    else if (byteArray[0].equals("00001000"))
    {
      Serial.println("SERVO1 Write");
      int value = byteStringToDenary(byteArray[2]);
      servo_1.write(value);
    }
  }
}
