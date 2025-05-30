import serial
import json
import time

def read_gps_from_serial(port="/dev/ttyACM0", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        last_known_location = {
            'lat': 0.0,
            'lng': 0.0,
            'orientation': 0.0,
            'speed': 0.0
        }
        print("Entro en read GPS from Serial")
        while True:
            try:
                line = ser.readline().decode('ascii', errors='replace').strip()
                if not line:
                    continue

                msg = json.loads(line)

                location = {
                    'lat': msg.get('lat', last_known_location['lat']),
                    'lng': msg.get('lng', last_known_location['lng']),
                    'orientation': msg.get('orientation', last_known_location['orientation']),
                    'speed': msg.get('speed', last_known_location['speed'])
                }

                last_known_location = location
                print(location)

            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error al leer datos: {e}")

            time.sleep(0.1)  # Pequeño retraso para evitar uso excesivo de CPU

    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto serial: {e}")
