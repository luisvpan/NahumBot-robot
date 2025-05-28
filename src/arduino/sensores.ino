#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <QMC5883LCompass.h>

#define TdsSensorPin A0
#define TurbiditySensorPin A1
#define VREF 5.0   // Voltaje de referencia analógica (Voltios) del ADC
#define SCOUNT 30  // Número de muestras para el sensor TDS

// Objetos para los sensores GY-87
Adafruit_BMP085 bmp;
QMC5883LCompass compass;

// Variables para el sensor TDS
int analogBuffer[SCOUNT];  // Almacena el valor analógico en el array, leído desde ADC
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0, copyIndex = 0;
float averageVoltage = 0, tdsValue = 0, temperature = 25;

// Variables para la comunicación serial
String inputString = "";      // String para almacenar los datos entrantes
bool stringComplete = false;  // Bandera para indicar cuando el string está completo

#define BombaPin1 6  // Pin para la primera bomba
#define BombaPin2 7  // Pin para la segunda bomba

// Funciones para controlar las bombas de agua
void setModo(String modo) {
  if (modo.equalsIgnoreCase("ninguno")) {
    digitalWrite(BombaPin1, HIGH);
    digitalWrite(BombaPin2, HIGH);
    Serial.println("Modo: NINGUNO - Ambas bombas están apagadas");
  } else if (modo.equalsIgnoreCase("vaciar")) {
    digitalWrite(BombaPin1, HIGH);
    digitalWrite(BombaPin2, LOW);
    Serial.println("Modo: VACIAR - Bomba 1 apagada, Bomba 2 encendida");
  } else if (modo.equalsIgnoreCase("llenar")) {
    digitalWrite(BombaPin1, LOW);
    digitalWrite(BombaPin2, HIGH);
    Serial.println("Modo: LLENAR - Bomba 1 encendida, Bomba 2 apagada");
  } else {
    Serial.println("Modo no reconocido. Comandos disponibles: 'ninguno', 'vaciar', 'llenar'");
  }
}

String estadoBomba() {
  String estado1 = digitalRead(BombaPin1) == LOW ? "Bomba 1: on" : "Bomba 1: off";
  String estado2 = digitalRead(BombaPin2) == LOW ? "Bomba 2: on" : "Bomba 2: off";
  return estado1 + ", " + estado2;
}
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

  // Configura los pines
  pinMode(TdsSensorPin, INPUT);
  pinMode(TurbiditySensorPin, INPUT);

  pinMode(BombaPin1, OUTPUT);
  pinMode(BombaPin2, OUTPUT);

  // Reserva 200 bytes para el inputString
  inputString.reserve(200);

  // Mensaje de inicio
  Serial.println("Sistema de sensores iniciado. Envía comandos para obtener lecturas.");
  Serial.println("Comandos disponibles: 'tds', 'turbidez', 'gy87', 'todos', 'bomba on', 'bomba off', 'bomba estado'");
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

  // Procesa los comandos seriales cuando están completos
  if (stringComplete) {
    inputString.trim();

    if (inputString.equalsIgnoreCase("tds")) {
      sendTDSValue();
    } else if (inputString.equalsIgnoreCase("turbidez")) {
      sendTurbidityValue();
    } else if (inputString.equalsIgnoreCase("gy87")) {
      sendGY87Values();
    } else if (inputString.equalsIgnoreCase("todos")) {
      sendAllSensors();
    } else if (inputString.equalsIgnoreCase("bomba estado")) {
      Serial.print("BOMBA: ");
      Serial.println(estadoBomba());
    } else if (inputString.equalsIgnoreCase("ninguno") || inputString.equalsIgnoreCase("vaciar") || inputString.equalsIgnoreCase("llenar")) {
      setModo(inputString);
    } else {
      Serial.println("Comando no reconocido. Comandos disponibles: 'tds', 'turbidez', 'gy87', 'todos', 'bomba on', 'bomba off', 'bomba estado'");
    }

    inputString = "";
    stringComplete = false;
  }
}

// Función para calcular y enviar el valor TDS
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
  if (!bmp.begin()) {
    Serial.println("ERROR: No se pudo inicializar el BMP180");
    return;
  }

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

// Función para enviar todos los valores de sensores
void sendAllSensors() {
  sendTDSValue();
  sendTurbidityValue();
  sendGY87Values();
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
