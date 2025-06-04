#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <QMC5883LCompass.h>
#include <OneWire.h>                
#include <DallasTemperature.h>

#define TdsSensorPin A0
#define TurbiditySensorPin A1
#define pHSensorPin A2
#define OneWireBusPin1 2 
#define OneWireBusPin2 3
#define VREF 5.0   // Voltaje de referencia analógica (Voltios) del ADC
#define SCOUNT 30  // Número de muestras para el sensor TDS

// Objetos para los sensores GY-87
Adafruit_BMP085 bmp;
QMC5883LCompass compass;

// Objetos para los sensores de temperatura independientes
OneWire oneWire1(OneWireBusPin1);
DallasTemperature sensorTemp1(&oneWire1);

OneWire oneWire2(OneWireBusPin2);
DallasTemperature sensorTemp2(&oneWire2);

// Variables para el sensor TDS
int analogBuffer[SCOUNT];  // Almacena el valor analógico en el array, leído desde ADC
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0, copyIndex = 0;
float averageVoltage = 0, tdsValue = 0, temperature = 25;

// Variables para la comunicación serial
String inputString = "";      // String para almacenar los datos entrantes
bool stringComplete = false;  // Bandera para indicar cuando el string está completo

void setup() {
  // Inicializa la comunicación serial con la Raspberry Pi
  Serial.begin(9600);

  // Inicializa I2C
  Wire.begin();

  // Inicializa BMP180
  if (!bmp.begin()) {
    Serial.println("Error al inicializar BMP180");
  }

  // Inicializa QMC5883L
  compass.init();
  compass.setCalibration(-1200, 1200, -1200, 1200, -1200, 1200);

  // Inicializa los sensores de temperatura independientes
  sensorTemp1.begin();
  sensorTemp2.begin();

  // Configura los pines de sensores analógicos
  pinMode(TdsSensorPin, INPUT);
  pinMode(TurbiditySensorPin, INPUT);
  pinMode(pHSensorPin, INPUT); // Configurar el sensor de pH

  inputString.reserve(200);
}

void loop() {
  // Lectura del sensor TDS
  static unsigned long analogSampleTimepoint = millis();
  if (millis() - analogSampleTimepoint > 40U) {
    analogSampleTimepoint = millis();
    analogBuffer[analogBufferIndex] = analogRead(TdsSensorPin);
    analogBufferIndex++;
    if (analogBufferIndex == SCOUNT) {
      analogBufferIndex = 0;
    }
  }

  // Leer datos del puerto serie
  while (Serial.available()) {
    char incomingChar = (char)Serial.read();
    inputString += incomingChar;

    // Verifica si se ha recibido un salto de línea (indica el final del comando)
    if (incomingChar == '\n') {
      stringComplete = true;
    }
  }

  // Procesa los comandos seriales cuando están completos
  if (stringComplete) {
    inputString.trim();

    if (inputString.equalsIgnoreCase("tds")) {
      sendTDSValue();
    } else if (inputString.equalsIgnoreCase("turbidez")) {
      sendTurbidityValue();
    } else if (inputString.equalsIgnoreCase("gy87")) {
      sendGY87Values();
    } else if (inputString.equalsIgnoreCase("ph")) {
      sendPHValue();
    } else if (inputString.equalsIgnoreCase("temp1")) {
      sendTemperatureValue(1);
    } else if (inputString.equalsIgnoreCase("temp2")) {
      sendTemperatureValue(2);
    } else if (inputString.equalsIgnoreCase("todos")) {
      sendAllSensors();
    }

    inputString = "";
    stringComplete = false;
  }
}

void sendTDSValue() {
  for (copyIndex = 0; copyIndex < SCOUNT; copyIndex++) {
    analogBufferTemp[copyIndex] = analogBuffer[copyIndex];
  }

  averageVoltage = getMedianNum(analogBufferTemp, SCOUNT) * (float)VREF / 1024.0;
  float compensationCoefficient = 1.0 + 0.02 * (temperature - 25.0);
  float compensationVolatge = averageVoltage / compensationCoefficient;
  tdsValue = (133.42 * compensationVolatge * compensationVolatge * compensationVolatge - 255.86 * compensationVolatge * compensationVolatge + 857.39 * compensationVolatge) * 0.5;

  Serial.print("TDS:");
  Serial.println(tdsValue, 0);
}

// Función para leer y enviar el valor de turbidez
void sendTurbidityValue() {
  int turbidityValue = analogRead(TurbiditySensorPin);
  Serial.print("TURBIDEZ:");
  Serial.println(turbidityValue);
}

// Función para enviar los valores del sensor GY-87
void sendGY87Values() {
  if (!bmp.begin()) return;

  float temperatura = bmp.readTemperature();
  float presion = bmp.readPressure() / 100.0;

  compass.read();
  int x = compass.getX();
  int y = compass.getY();
  int z = compass.getZ();

  Serial.print("GY87:{");
  Serial.print("\"temperatura\":");
  Serial.print(temperatura);
  Serial.print(",\"presion\":");
  Serial.print(presion);
  Serial.print(",\"magnetometro\":{");
  Serial.print("\"x\":");
  Serial.print(x);
  Serial.print(",\"y\":");
  Serial.print(y);
  Serial.print(",\"z\":");
  Serial.print(z);
  Serial.println("}}");
}

void sendPHValue() {
  float voltage = analogRead(pHSensorPin) * (VREF / 1023.0);
  float pH = 3.5 * voltage;  // Ajustar según calibración específica
  Serial.print("PH:");
  Serial.println(pH);
}

// Enviar temperatura por sensor 1 o 2, según índice
void sendTemperatureValue(int sensorNum) {
  if (sensorNum == 1) {
    sensorTemp1.requestTemperatures();
    delay(750);  // Esperar a que el sensor termine la conversión
    float temp1 = sensorTemp1.getTempCByIndex(0);
    Serial.print("TEMP1: ");
    Serial.println(temp1);
  } else if (sensorNum == 2) {
    sensorTemp2.requestTemperatures();
    delay(750);  // Esperar a que el sensor termine la conversión
    float temp2 = sensorTemp2.getTempCByIndex(0);
    Serial.print("TEMP2: ");
    Serial.println(temp2);
  }
}

void sendAllSensors() {
  // Solicitar temperaturas de ambos sensores simultáneamente
  sensorTemp1.requestTemperatures();
  sensorTemp2.requestTemperatures();
  
  // Esperar a que ambos sensores terminen la conversión
  delay(750);  // Los DS18B20 necesitan aproximadamente 750ms para la conversión
  
  // Enviar el resto de los datos
  sendTDSValue();
  sendTurbidityValue();
  sendPHValue();
  sendGY87Values();
  
  // Enviar las temperaturas que ya están listas
  float temp1 = sensorTemp1.getTempCByIndex(0);
  float temp2 = sensorTemp2.getTempCByIndex(0);
  
  Serial.print("TEMP1: ");
  Serial.println(temp1);
  Serial.print("TEMP2: ");
  Serial.println(temp2);
}

// Función auxiliar para calcular la mediana
int getMedianNum(int bArray[], int iFilterLen) {
  int bTab[iFilterLen];
  for (byte i = 0; i < iFilterLen; i++) {
    bTab[i] = bArray[i];
  }

  int i, j, bTemp;
  for (j = 0; j < iFilterLen - 1; j++) {
    for (i = 0; i < iFilterLen - j - 1; i++) {
      if (bTab[i] > bTab[i + 1]) {
        bTemp = bTab[i];
        bTab[i] = bTab[i + 1];
        bTab[i + 1] = bTemp;
      }
    }
  }

  return (iFilterLen & 1) ? bTab[(iFilterLen - 1) / 2] : (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
}
