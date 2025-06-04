import serial
import time
import sys
from constants import is_simulation_mode
import random
import json

class ArduinoSensorInterface:
    def __init__(self, port='/dev/serial0', baud_rate=9600, timeout=2):
        """
        Inicializa la interfaz de comunicación con Arduino.
        
        Args:
            port (str): Puerto serial donde está conectado el Arduino (por defecto en Raspberry Pi: '/dev/ttyACM0')
            baud_rate (int): Velocidad de comunicación (debe coincidir con el Arduino)
            timeout (int): Tiempo de espera en segundos para la respuesta
        """
        if (is_simulation_mode):
            print("Modo simulacion")
        else:
            try:
                self.serial_conn = serial.Serial(port, baud_rate, timeout=timeout)
                time.sleep(2)  # Espera a que se inicialice la conexión con Arduino
                print(f"Conexión establecida con Arduino en {port}")
                
                # Leer mensajes iniciales del Arduino
                self._flush_input()
            except serial.SerialException as e:
                print(f"Error al conectar con Arduino: {e}")
                sys.exit(1)
    
    def _flush_input(self):
        """Limpia el buffer de entrada para eliminar datos antiguos"""
        time.sleep(0.5)
        while self.serial_conn.in_waiting:
            print(f"Mensaje de Arduino: {self.serial_conn.readline().decode('utf-8').strip()}")
            time.sleep(0.1)
    
    def get_sensor_data(self, sensor_type):
        """
        Solicita datos de un sensor específico o de todos los sensores.
        
        Args:
            sensor_type (str): Tipo de sensor ('tds', 'turbidez', 'todos', 'bombaestado')
            
        Returns:
            dict: Diccionario con los valores de los sensores solicitados
        """

        if (is_simulation_mode):
            if sensor_type == 'bombaestado':
                return {'bomba1': 'on', 'bomba2': 'on'}  # Simulación de estado de bombas
            turbidez = random.random()  # Variación controlada para turbidez
            tds = random.random()
            return {'turbidez': turbidez, 'tds': tds}
        
        else:
            valid_types = ['tds', 'turbidez', 'todos', 'bombaestado', 'llenar', 'vaciar', 'ninguno']
            if sensor_type.lower() not in valid_types:
                print(f"Tipo de sensor no válido. Opciones: {', '.join(valid_types)}")
                return None
            
            # Limpia el buffer antes de enviar una nueva solicitud
            self._flush_input()
            
            # Envía el comando al Arduino
            self.serial_conn.write(f"{sensor_type.lower()}\n".encode('utf-8'))
            
            # Espera y recoge la respuesta
            time.sleep(0.5)
            
            # Procesa los datos recibidos
            result = {}
            while self.serial_conn.in_waiting:
                response = self.serial_conn.readline().decode('utf-8').strip()
                print("response: ",response)
                if sensor_type == 'bombaestado':
                    response = response.strip()
                    result = {}
                    
                    # Divide la respuesta en partes
                    bombas = response.split(", ")
                   
                    # Procesa cada bomba y su estado
                    for bomba in bombas:
                        nombre, estado = bomba.split(": ")
                        print("nombre ", nombre)
                        print("estado ", estado)
                        result[nombre.lower().replace(" ", "")] = estado.strip()
                    
                    return result

                if ':' in response:
                    key, value = response.split(':', 1)
                    key = key.lower().strip()  # Elimina espacios en blanco
                    value = value.strip()
                    print('key: ', key)
                    if key == 'tds':
                        result[key] = float(value)
                    elif key == 'turbidez':
                        result[key] = float(value)
                     # Almacena el estado de las bombas
                    else:
                        result[key] = float(value)  # Para otros sensores, convierte a int
                time.sleep(0.1)
            
            return result

            
    def close(self):
        """Cierra la conexión serial"""
        if hasattr(self, 'serial_conn') and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Conexión con Arduino cerrada")


# Ejemplo de uso
if __name__ == "__main__":
    arduino = ArduinoSensorInterface()
    
    try:
        while True:
            print("\nSelecciona una opción:")
            print("1. Leer sensor TDS")
            print("2. Leer sensor de Turbidez")
            print("3. Leer todos los sensores")
            print("4. Salir")
            
            option = input("Opción: ")
            
            if option == '1':
                tds_data = arduino.get_sensor_data('tds')
                if tds_data and 'tds' in tds_data:
                    print(f"Valor TDS: {tds_data['tds']} ppm")
                else:
                    print("No se pudo obtener el valor TDS")
            
            elif option == '2':
                turbidity_data = arduino.get_sensor_data('turbidez')
                if turbidity_data and 'turbidez' in turbidity_data:
                    print(f"Valor de Turbidez: {turbidity_data['turbidez']}")
                else:
                    print("No se pudo obtener el valor de Turbidez")
            
            elif option == '3':
                all_data = arduino.get_sensor_data('todos')
                if all_data:
                    for sensor, value in all_data.items():
                        unit = "ppm" if sensor == "tds" else ""
                        print(f"Valor de {sensor.upper()}: {value} {unit}")
                else:
                    print("No se pudieron obtener los valores de los sensores")
            
            elif option == '4':
                break
            
            else:
                print("Opción no válida")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nPrograma finalizado por el usuario")
    
    finally:
        arduino.close()