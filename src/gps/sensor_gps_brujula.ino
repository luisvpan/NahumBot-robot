#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <SoftwareSerial.h>

SoftwareSerial gps(4, 3);
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
char dato = ' ';

void setup() 
{
  Serial.begin(9600);
  gps.begin(9600);

  if (!mag.begin()) 
  {
    Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
    while (1);
  }
}

void loop() 
{
  String gpsData = "";

  // Capturar datos del GPS
  while (gps.available()) 
  {
    dato = gps.read();
    gpsData += dato;
  }

  // Capturar datos de orientación
  sensors_event_t event;
  mag.getEvent(&event);
  float heading = atan2(event.magnetic.y, event.magnetic.x);

  // Ajustar la declinación magnética
  float declinationAngle = 0.22;
  heading += declinationAngle;

  if (heading < 0) heading += 2 * PI;
  if (heading > 2 * PI) heading -= 2 * PI;

  float headingDegrees = heading * 180 / M_PI;

  // Imprimir datos en una sola línea
  Serial.print(gpsData);
  delay(1000);
  Serial.println("");
  Serial.print("Ori: ");
  Serial.println(headingDegrees);
  
  delay(500);
}
